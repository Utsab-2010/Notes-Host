/**
 * Everforest Digital Garden Interactive Features
 * Modeled after Quartz (glennklockwood.com/garden) & Obsidian
 */

(function () {
    'use strict';

    // ==========================================
    // 1. Sidebar, Search & Folder Navigation
    // ==========================================
    window.toggleSidebar = function () {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) sidebar.classList.toggle('active');
    };

    window.focusSearch = function () {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && !sidebar.classList.contains('active') && window.innerWidth < 850) {
            sidebar.classList.add('active');
        }
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    };

    window.toggleFolder = function (headerElement, event) {
        if (event.target.tagName.toLowerCase() === 'a') {
            return;
        }
        event.preventDefault();
        event.stopPropagation();

        const folderItem = headerElement.closest('.tree-item.folder');
        if (!folderItem) return;

        const content = folderItem.querySelector('.folder-content');
        if (!content) return;

        const isCurrentlyOpen = folderItem.classList.contains('open');
        if (isCurrentlyOpen) {
            content.style.display = 'none';
            folderItem.classList.remove('open');
        } else {
            content.style.display = 'block';
            folderItem.classList.add('open');
        }
    };

    let allFoldersExpanded = true;
    window.toggleAllFolders = function () {
        const folders = document.querySelectorAll('.tree-item.folder');
        const toggleBtnText = document.getElementById('toggle-all-text');
        allFoldersExpanded = !allFoldersExpanded;

        folders.forEach(f => {
            const content = f.querySelector('.folder-content');
            if (!content) return;
            if (allFoldersExpanded) {
                f.classList.add('open');
                content.style.display = 'block';
            } else {
                f.classList.remove('open');
                content.style.display = 'none';
            }
        });

        if (toggleBtnText) {
            toggleBtnText.textContent = allFoldersExpanded ? 'Collapse' : 'Expand';
        }
    };

    window.filterTree = function () {
        const input = document.getElementById('search-input');
        if (!input) return;
        const query = input.value.toLowerCase().trim();
        const items = document.querySelectorAll('.file-title-link, .folder-title');

        if (!query) {
            document.querySelectorAll('.tree-item').forEach(item => {
                item.style.display = '';
            });
            document.querySelectorAll('.folder-content').forEach(content => {
                const folderItem = content.closest('.tree-item.folder');
                if (folderItem && folderItem.classList.contains('open')) {
                    content.style.display = 'block';
                } else if (folderItem) {
                    content.style.display = 'none';
                }
            });
            return;
        }

        document.querySelectorAll('.tree-item').forEach(item => {
            item.style.display = 'none';
        });

        items.forEach(el => {
            const text = el.textContent.toLowerCase();
            if (text.includes(query)) {
                const item = el.closest('.tree-item');
                if (item) {
                    item.style.display = '';
                    let parent = item.parentElement.closest('.tree-item.folder');
                    while (parent) {
                        parent.style.display = '';
                        parent.classList.add('open');
                        const content = parent.querySelector('.folder-content');
                        if (content) content.style.display = 'block';
                        parent = parent.parentElement.closest('.tree-item.folder');
                    }
                }
            }
        });
    };

    // Keyboard shortcut '/' or 'Ctrl+K' to focus search
    document.addEventListener('keydown', function (e) {
        if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && 
            !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
            e.preventDefault();
            window.focusSearch();
        }
    });

    // ==========================================
    // 2. Obsidian Callouts Transformer
    // ==========================================
    function transformCallouts() {
        const blockquotes = document.querySelectorAll('.markdown-body blockquote');
        const calloutIcons = {
            note: '📝',
            abstract: '📋',
            summary: '📋',
            tldr: '📋',
            info: 'ℹ️',
            todo: '☑️',
            tip: '💡',
            hint: '💡',
            important: '🔥',
            success: '✅',
            check: '✅',
            done: '✅',
            question: '❓',
            help: '❓',
            faq: '❓',
            warning: '⚠️',
            caution: '⚠️',
            attention: '⚠️',
            failure: '❌',
            fail: '❌',
            missing: '❌',
            danger: '🚨',
            error: '🚨',
            bug: '🐛',
            example: '🔍',
            quote: '💬',
            cite: '💬'
        };

        blockquotes.forEach(bq => {
            const firstP = bq.querySelector('p');
            if (!firstP) return;

            const text = firstP.textContent.trim();
            const match = text.match(/^\[!([a-zA-Z0-9_-]+)\]([+-])?\s*(.*)?$/);
            if (!match) return;

            const type = match[1].toLowerCase();
            const icon = calloutIcons[type] || '📝';
            const rawTitle = match[3] ? match[3].trim() : type.charAt(0).toUpperCase() + type.slice(1);

            // Clean the first paragraph
            const regexClean = new RegExp('^\\[!' + match[1] + '\\][+-]?\\s*' + (match[3] ? escapeRegExp(match[3]) : ''), 'i');
            firstP.innerHTML = firstP.innerHTML.replace(regexClean, '').trim();

            // Create callout wrapper
            const callout = document.createElement('div');
            callout.className = `callout callout-${type}`;

            const header = document.createElement('div');
            header.className = 'callout-header';
            header.innerHTML = `
                <span class="callout-icon">${icon}</span>
                <span class="callout-title">${escapeHtml(rawTitle)}</span>
            `;

            const body = document.createElement('div');
            body.className = 'callout-body';

            while (bq.firstChild) {
                body.appendChild(bq.firstChild);
            }

            callout.appendChild(header);
            callout.appendChild(body);
            bq.parentNode.replaceChild(callout, bq);
        });
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function escapeHtml(string) {
        return string.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // ==========================================
    // 3. Code Blocks Header & Copy Button
    // ==========================================
    function enhanceCodeBlocks() {
        const pres = document.querySelectorAll('.markdown-body pre');
        pres.forEach(pre => {
            if (pre.parentElement && pre.parentElement.classList.contains('code-block-wrapper')) {
                return;
            }

            const code = pre.querySelector('code');
            let lang = 'code';
            if (code) {
                const classes = code.className.split(' ');
                for (const cls of classes) {
                    if (cls.startsWith('language-')) {
                        lang = cls.replace('language-', '');
                        break;
                    }
                }
            }

            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';

            const header = document.createElement('div');
            header.className = 'code-header';

            const langBadge = document.createElement('span');
            langBadge.className = 'code-lang-badge';
            langBadge.textContent = lang.toUpperCase();

            const copyBtn = document.createElement('button');
            copyBtn.className = 'code-copy-btn';
            copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
            copyBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="copy-svg">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span class="copy-text">Copy</span>
            `;

            copyBtn.addEventListener('click', () => {
                const textToCopy = code ? code.innerText : pre.innerText;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    copyBtn.classList.add('copied');
                    copyBtn.querySelector('.copy-text').textContent = 'Copied!';
                    setTimeout(() => {
                        copyBtn.classList.remove('copied');
                        copyBtn.querySelector('.copy-text').textContent = 'Copy';
                    }, 2000);
                }).catch(err => {
                    console.error('Copy failed:', err);
                });
            });

            header.appendChild(langBadge);
            header.appendChild(copyBtn);

            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(header);
            wrapper.appendChild(pre);
        });
    }

    // ==========================================
    // 4. Table of Contents (TOC) Scrollspy
    // ==========================================
    function initScrollspy() {
        const tocLinks = document.querySelectorAll('.toc-content a');
        if (!tocLinks.length) return;

        const headingMap = new Map();
        tocLinks.forEach(link => {
            const hash = decodeURIComponent(link.getAttribute('href') || '');
            if (hash.startsWith('#')) {
                const id = hash.slice(1);
                const el = document.getElementById(id);
                if (el) headingMap.set(el, link);
            }
        });

        if (!headingMap.size) return;

        let activeLink = null;
        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const link = headingMap.get(entry.target);
                        if (link && link !== activeLink) {
                            if (activeLink) activeLink.classList.remove('active');
                            link.classList.add('active');
                            activeLink = link;
                        }
                    }
                });
            },
            { rootMargin: '0px 0px -70% 0px', threshold: 0.1 }
        );

        headingMap.forEach((link, heading) => observer.observe(heading));
    }

    // ==========================================
    // 5. Quartz-style Hover Popovers (Link Previews)
    // ==========================================
    function initHoverPopovers() {
        const popover = document.getElementById('garden-popover');
        if (!popover) return;

        const popoverTitle = popover.querySelector('.popover-title');
        const popoverBody = popover.querySelector('.popover-body');
        const internalLinks = document.querySelectorAll('.markdown-body a');
        const cache = new Map();

        let hoverTimer = null;
        let currentTarget = null;

        internalLinks.forEach(link => {
            const href = link.getAttribute('href');
            // Check if internal note link
            if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto')) {
                return;
            }
            if (!href.includes('/vault/') && !href.startsWith('/')) {
                return;
            }

            link.classList.add('internal-note-link');

            link.addEventListener('mouseenter', e => {
                clearTimeout(hoverTimer);
                currentTarget = link;

                hoverTimer = setTimeout(() => {
                    showPreview(href, link);
                }, 250);
            });

            link.addEventListener('mouseleave', () => {
                clearTimeout(hoverTimer);
                hoverTimer = setTimeout(() => {
                    if (!popover.matches(':hover')) {
                        hidePreview();
                    }
                }, 200);
            });
        });

        popover.addEventListener('mouseleave', () => {
            hidePreview();
        });

        function showPreview(url, anchorEl) {
            popover.style.display = 'block';
            popoverTitle.textContent = 'Loading...';
            popoverBody.textContent = 'Fetching preview...';

            positionPopover(anchorEl);

            if (cache.has(url)) {
                renderPreview(cache.get(url));
            } else {
                fetch(url)
                    .then(res => res.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const titleEl = doc.querySelector('.note-title') || doc.querySelector('h1');
                        const title = titleEl ? titleEl.textContent : url;

                        const contentEl = doc.querySelector('.markdown-body');
                        let snippet = '';
                        if (contentEl) {
                            const p = contentEl.querySelector('p');
                            snippet = p ? p.textContent.slice(0, 240) + '...' : 'No preview available.';
                        } else {
                            snippet = 'Digital garden note.';
                        }

                        const data = { title, snippet };
                        cache.set(url, data);
                        if (currentTarget === anchorEl) {
                            renderPreview(data);
                        }
                    })
                    .catch(err => {
                        popoverTitle.textContent = 'Note Preview';
                        popoverBody.textContent = 'Click to open note.';
                    });
            }
        }

        function renderPreview(data) {
            popoverTitle.textContent = data.title;
            popoverBody.textContent = data.snippet;
            popover.classList.add('visible');
        }

        function hidePreview() {
            popover.classList.remove('visible');
            setTimeout(() => {
                if (!popover.classList.contains('visible')) {
                    popover.style.display = 'none';
                }
            }, 200);
        }

        function positionPopover(anchorEl) {
            const rect = anchorEl.getBoundingClientRect();
            const popoverWidth = 320;
            const padding = 15;

            let left = rect.left;
            let top = rect.bottom + 8;

            if (left + popoverWidth > window.innerWidth - padding) {
                left = window.innerWidth - popoverWidth - padding;
            }
            if (left < padding) left = padding;

            if (top + 180 > window.innerHeight - padding) {
                top = rect.top - 180 - 8;
            }

            popover.style.left = `${Math.round(left)}px`;
            popover.style.top = `${Math.round(top)}px`;
        }
    }

    // ==========================================
    // 6. Interactive Local Force Knowledge Graph
    // ==========================================
    function initLocalGraph() {
        const canvas = document.getElementById('local-graph-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Current note identifier
        const currentPath = window.location.pathname.replace(/\/index\.html$/, '').replace(/\/$/, '') + '/';

        fetch('/graph.json')
            .catch(() => fetch('../graph.json'))
            .then(res => res.json())
            .then(graph => {
                setupGraphVisualization(canvas, ctx, graph, currentPath);
            })
            .catch(err => {
                console.log('Graph data note: static/graph.json loading in local mode', err);
            });
    }

    function setupGraphVisualization(canvas, ctx, graph, currentPath) {
        const width = canvas.width;
        const height = canvas.height;

        // Find current node
        let currentSlug = currentPath.toLowerCase();
        let targetNode = graph.nodes.find(n => n.id.toLowerCase() === currentSlug || currentSlug.includes(n.id.toLowerCase()));

        if (!targetNode && graph.nodes.length > 0) {
            targetNode = graph.nodes[0];
        }

        if (!targetNode) return;

        // Find 1-hop connected nodes
        const connectedIds = new Set();
        connectedIds.add(targetNode.id);

        const subLinks = [];
        graph.links.forEach(l => {
            const src = typeof l.source === 'object' ? l.source.id : l.source;
            const tgt = typeof l.target === 'object' ? l.target.id : l.target;

            if (src.toLowerCase() === targetNode.id.toLowerCase()) {
                connectedIds.add(tgt);
                subLinks.push({ source: targetNode.id, target: tgt });
            } else if (tgt.toLowerCase() === targetNode.id.toLowerCase()) {
                connectedIds.add(src);
                subLinks.push({ source: src, target: targetNode.id });
            }
        });

        // Filter nodes
        const subNodes = graph.nodes
            .filter(n => connectedIds.has(n.id))
            .map(n => ({
                id: n.id,
                title: n.title,
                isCurrent: n.id.toLowerCase() === targetNode.id.toLowerCase(),
                x: width / 2 + (Math.random() - 0.5) * 80,
                y: height / 2 + (Math.random() - 0.5) * 80,
                vx: 0,
                vy: 0,
                radius: n.id.toLowerCase() === targetNode.id.toLowerCase() ? 7 : 4.5
            }));

        const nodeMap = new Map();
        subNodes.forEach(n => nodeMap.set(n.id, n));

        const simLinks = subLinks
            .filter(l => nodeMap.has(l.source) && nodeMap.has(l.target))
            .map(l => ({
                source: nodeMap.get(l.source),
                target: nodeMap.get(l.target)
            }));

        let hoveredNode = null;

        canvas.addEventListener('mousemove', e => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            hoveredNode = null;
            for (const n of subNodes) {
                const dist = Math.hypot(n.x - mouseX, n.y - mouseY);
                if (dist <= n.radius + 4) {
                    hoveredNode = n;
                    canvas.style.cursor = 'pointer';
                    break;
                }
            }
            if (!hoveredNode) {
                canvas.style.cursor = 'default';
            }
        });

        canvas.addEventListener('click', () => {
            if (hoveredNode && !hoveredNode.isCurrent) {
                window.location.href = hoveredNode.id;
            }
        });

        let iterations = 0;
        function stepSimulation() {
            // Repulsion between nodes
            for (let i = 0; i < subNodes.length; i++) {
                for (let j = i + 1; j < subNodes.length; j++) {
                    const a = subNodes[i];
                    const b = subNodes[j];
                    const dx = b.x - a.x;
                    const dy = b.y - a.y;
                    const dist = Math.hypot(dx, dy) || 1;
                    const force = 180 / (dist * dist);
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;
                    a.vx -= fx;
                    a.vy -= fy;
                    b.vx += fx;
                    b.vy += fy;
                }
            }

            // Spring force along links
            simLinks.forEach(l => {
                const dx = l.target.x - l.source.x;
                const dy = l.target.y - l.source.y;
                const dist = Math.hypot(dx, dy) || 1;
                const springForce = (dist - 48) * 0.05;
                const fx = (dx / dist) * springForce;
                const fy = (dy / dist) * springForce;
                l.source.vx += fx;
                l.source.vy += fy;
                l.target.vx -= fx;
                l.target.vy -= fy;
            });

            // Center gravity
            subNodes.forEach(n => {
                if (n.isCurrent) {
                    n.vx += (width / 2 - n.x) * 0.1;
                    n.vy += (height / 2 - n.y) * 0.1;
                } else {
                    n.vx += (width / 2 - n.x) * 0.015;
                    n.vy += (height / 2 - n.y) * 0.015;
                }
                n.vx *= 0.85;
                n.vy *= 0.85;
                n.x += n.vx;
                n.y += n.vy;

                // Bounds
                n.x = Math.max(n.radius + 4, Math.min(width - n.radius - 4, n.x));
                n.y = Math.max(n.radius + 4, Math.min(height - n.radius - 4, n.y));
            });

            // Render
            ctx.clearRect(0, 0, width, height);

            // Draw links
            ctx.lineWidth = 1.2;
            simLinks.forEach(l => {
                ctx.beginPath();
                ctx.moveTo(l.source.x, l.source.y);
                ctx.lineTo(l.target.x, l.target.y);
                ctx.strokeStyle = 'rgba(167, 192, 128, 0.22)';
                ctx.stroke();
            });

            // Draw nodes
            subNodes.forEach(n => {
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);

                if (n.isCurrent) {
                    ctx.fillStyle = '#a7c080'; // Everforest spring green
                    ctx.shadowColor = 'rgba(167, 192, 128, 0.5)';
                    ctx.shadowBlur = 8;
                } else if (n === hoveredNode) {
                    ctx.fillStyle = '#7fbbb3'; // stream aqua
                    ctx.shadowColor = 'rgba(127, 187, 179, 0.5)';
                    ctx.shadowBlur = 6;
                } else {
                    ctx.fillStyle = '#83c092'; // soft eucalyptus
                    ctx.shadowBlur = 0;
                }
                ctx.fill();
                ctx.shadowBlur = 0;

                // Draw label for current or hovered node
                if (n.isCurrent || n === hoveredNode) {
                    ctx.font = '10px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
                    ctx.fillStyle = '#d3c6aa';
                    const text = n.title.length > 20 ? n.title.slice(0, 18) + '...' : n.title;
                    ctx.fillText(text, n.x + 8, n.y + 3);
                }
            });

            iterations++;
            if (iterations < 280 || hoveredNode) {
                requestAnimationFrame(stepSimulation);
            }
        }

        requestAnimationFrame(stepSimulation);
    }

    // ==========================================
    // Initialization on Page Load
    // ==========================================
    document.addEventListener('DOMContentLoaded', () => {
        transformCallouts();
        enhanceCodeBlocks();
        initScrollspy();
        initHoverPopovers();
        initLocalGraph();
    });
})();

