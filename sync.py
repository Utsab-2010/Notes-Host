import os
import sys
import re
import shutil
import time

VAULT_DIR = os.environ.get("VAULT_DIR", "/home/utsab/Utsab-Notes")
CONTENT_DIR = os.environ.get("CONTENT_DIR", "/home/utsab/notes-hosted/hugo-site/content/vault")
CONFIG_FILE = "/home/utsab/notes-hosted/hugo-site/config.toml"

# Exclude lists
EXCLUDE_DIRS = {'.git', '.obsidian', 'Journal'}
EXCLUDE_FILES = {'Internship Applications.md', 'Project Ideas.md', 'Vault Content.base'}

def slugify(text):
    text = text.lower()
    # Replace spaces and underscores with dashes
    text = re.sub(r'[\s_]+', '-', text)
    # Remove any non-alphanumeric chars except dashes
    text = re.sub(r'[^a-z0-9\-]', '', text)
    # Remove multiple dashes
    text = re.sub(r'-+', '-', text)
    return text

def get_hugo_url_path(rel_path):
    # Convert vault relative path to slugified Hugo URL
    # E.g. "Deep Learning/Neural Implicit Fields.md" -> "/vault/deep-learning/neural-implicit-fields/"
    parts = rel_path.split(os.sep)
    slugified_parts = []
    for part in parts:
        name, ext = os.path.splitext(part)
        slugified_parts.append(slugify(name))
    return "/vault/" + "/".join(slugified_parts) + "/"

def build_indices():
    note_map = {} # title -> url
    resource_map = {} # filename -> url
    
    for root, dirs, files in os.walk(VAULT_DIR):
        # Filter excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file in EXCLUDE_FILES:
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, VAULT_DIR)
            
            if file.endswith('.md'):
                title = os.path.splitext(file)[0]
                url = get_hugo_url_path(rel_path)
                note_map[title.lower()] = url
            else:
                # E.g. image.png -> /vault/Assets/Images/image.png
                parts = rel_path.split(os.sep)
                slugified_parts = [slugify(os.path.splitext(p)[0]) + os.path.splitext(p)[1] if idx == len(parts)-1 else slugify(p) for idx, p in enumerate(parts)]
                resource_map[file.lower()] = "/vault/" + "/".join(slugified_parts)
                
    return note_map, resource_map

def process_markdown(src_path, dest_path, note_map, resource_map):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Prepend frontmatter if missing
    if not content.strip().startswith('---'):
        title = os.path.splitext(os.path.basename(src_path))[0]
        clean_title = title.replace('"', '\\"')
        content = f"---\ntitle: \"{clean_title}\"\n---\n\n" + content

    # 2. Convert Obsidian Wikilink Images: ![[image.png]] or ![[image.png|width]]
    image_re = re.compile(r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
    
    def replace_image(match):
        filename = match.group(1).strip()
        alias = match.group(2).strip() if match.group(2) else ""
        lower_name = filename.lower()
        if lower_name in resource_map:
            return f"![{alias}]({resource_map[lower_name]})"
        return match.group(0) # Keep original if not found
        
    content = image_re.sub(replace_image, content)

    # 3. Convert Obsidian Internal Links: [[Note Name]] or [[Note Name|Alias]]
    link_re = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
    
    def replace_link(match):
        target = match.group(1).strip()
        alias = match.group(2).strip() if match.group(2) else target
        lower_target = target.lower()
        if lower_target in note_map:
            return f"[{alias}]({note_map[lower_target]})"
        return match.group(0) # Keep original if not found
        
    content = link_re.sub(replace_link, content)

    # Write processed file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)

def sync_all():
    print("Indexing vault...")
    note_map, resource_map = build_indices()
    
    print("Cleaning destination content/vault directory...")
    if os.path.exists(CONTENT_DIR):
        shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    
    # Write _index.md for the root vault directory
    with open(os.path.join(CONTENT_DIR, "_index.md"), 'w', encoding='utf-8') as f:
        f.write("---\ntitle: \"Vault\"\n---\n")
        
    print("Syncing files...")
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Create directories and write their _index.md to enable nested sections in Hugo
        for d in dirs:
            src_dir = os.path.join(root, d)
            rel_dir = os.path.relpath(src_dir, VAULT_DIR)
            dest_dir = os.path.join(CONTENT_DIR, rel_dir)
            os.makedirs(dest_dir, exist_ok=True)
            
            # Check if any parent directory is 'attachments' or 'assets'
            path_parts = [p.lower() for p in rel_dir.split(os.sep)]
            is_asset_dir = any(p in {'attachments', 'assets'} for p in path_parts)
            
            if not is_asset_dir:
                index_path = os.path.join(dest_dir, "_index.md")
                clean_title = d.replace('"', '\\"')
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(f"---\ntitle: \"{clean_title}\"\n---\n")
        
        for file in files:
            if file in EXCLUDE_FILES:
                continue
                
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, VAULT_DIR)
            dest_file = os.path.join(CONTENT_DIR, rel_path)
            
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            
            if file.endswith('.md'):
                # Process markdown (copy + rewrite links)
                process_markdown(src_file, dest_file, note_map, resource_map)
            else:
                # Symlink images/assets
                if os.path.exists(dest_file):
                    os.remove(dest_file)
                os.symlink(src_file, dest_file)
                
    print("Sync complete.")

def watch_vault():
    print(f"Watching {VAULT_DIR} for changes...")
    mtimes = {}
    
    # Initialize modification times
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file in EXCLUDE_FILES:
                continue
            path = os.path.join(root, file)
            mtimes[path] = os.path.getmtime(path)
            
    while True:
        try:
            time.sleep(1.5)
            changed = False
            current_files = set()
            
            for root, dirs, files in os.walk(VAULT_DIR):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                for file in files:
                    if file in EXCLUDE_FILES:
                        continue
                    path = os.path.join(root, file)
                    current_files.add(path)
                    
                    mtime = os.path.getmtime(path)
                    if path not in mtimes or mtime > mtimes[path]:
                        print(f"Change detected: {path}")
                        mtimes[path] = mtime
                        changed = True
            
            deleted_files = set(mtimes.keys()) - current_files
            if deleted_files:
                for path in deleted_files:
                    print(f"File deleted: {path}")
                    del mtimes[path]
                changed = True
                
            if changed:
                sync_all()
                
        except KeyboardInterrupt:
            print("\nStopping watcher.")
            break
        except Exception as e:
            print(f"Error in watcher: {e}")
            time.sleep(2)

if __name__ == '__main__':
    sync_all()
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        watch_vault()
