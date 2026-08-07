import os
import sys
import base64
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Configuration
PUBLIC_DIR = "public"
PASSWORD = os.environ.get("DECRYPT_PASSWORD") or "password"

PROTECTED_PREFIXES = [
    "vault/journal",
    "vault/misc",
    "vault/research-work",
    "vault/history",
    "vault/blogs",
    "vault/video-ideas",
    "vault/internship-applications",
    "vault/project-ideas",
    "vault/command-center"
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Vault - Password Required</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #14181a;
            font-family: 'Outfit', system-ui, -apple-system, sans-serif;
            color: #d3c6aa;
            overflow: hidden;
            position: relative;
        }

        /* Floating Gradient Blobs matching Everforest green/teal */
        .bg-glow {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }
        .blob {
            position: absolute;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            filter: blur(140px);
            opacity: 0.15;
            animation: float 25s infinite alternate ease-in-out;
        }
        .blob-1 {
            background: #8da874;
            top: -20%;
            left: -10%;
        }
        .blob-2 {
            background: #7fbbb3;
            bottom: -20%;
            right: -10%;
            animation-delay: -12s;
        }
        @keyframes float {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(120px, 90px) scale(1.15); }
            100% { transform: translate(-60px, 160px) scale(0.9); }
        }

        /* Card Styling using Everforest translucent base */
        .card-container {
            width: 90%;
            max-width: 420px;
            perspective: 1000px;
            opacity: 0;
            transform: translateY(20px);
            animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes slideUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .card {
            background: rgba(28, 34, 37, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(141, 168, 116, 0.15);
            border-radius: 28px;
            padding: 48px 40px;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .card:hover {
            border-color: rgba(141, 168, 116, 0.35);
            box-shadow: 0 24px 60px rgba(141, 168, 116, 0.08);
        }

        /* SVG Lock Icon */
        .icon-wrapper {
            margin-bottom: 24px;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            width: 72px;
            height: 72px;
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(141, 168, 116, 0.12);
            border-radius: 20px;
        }
        .lock-icon {
            width: 32px;
            height: 32px;
        }

        h1 {
            font-size: 24px;
            font-weight: 700;
            margin: 0 0 10px 0;
            color: #d3c6aa;
            letter-spacing: -0.5px;
        }
        p {
            font-size: 14px;
            color: #9da9a0;
            line-height: 1.6;
            margin: 0 0 32px 0;
        }

        /* Input styling matching Everforest inputs */
        .input-group {
            position: relative;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .input-group input {
            width: 100%;
            padding: 16px 48px 16px 20px;
            background: rgba(20, 24, 26, 0.6);
            border: 1px solid rgba(79, 92, 94, 0.4);
            border-radius: 14px;
            outline: none;
            color: #d3c6aa;
            font-family: inherit;
            font-size: 15px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-sizing: border-box;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        .input-group input:focus {
            border-color: #8da874;
            background: rgba(20, 24, 26, 0.8);
            box-shadow: 0 0 0 3px rgba(141, 168, 116, 0.2), inset 0 1px 2px rgba(0, 0, 0, 0.1);
        }

        /* Toggle password visibility */
        .toggle-password {
            position: absolute;
            right: 16px;
            background: none;
            border: none;
            cursor: pointer;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0.5;
            transition: opacity 0.2s, transform 0.2s;
        }
        .toggle-password:hover {
            opacity: 0.85;
            transform: scale(1.08);
        }

        /* Submit Button matching Everforest brand colors */
        button[type="submit"] {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #8da874 0%, #7fbbb3 100%);
            border: none;
            border-radius: 14px;
            color: #14181a;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 8px 24px rgba(141, 168, 116, 0.25);
            font-family: inherit;
        }
        button[type="submit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(141, 168, 116, 0.35);
            filter: brightness(1.05);
        }
        button[type="submit"]:active {
            transform: translateY(0);
        }

        /* Error Message & Shake */
        .error-message {
            color: #e67e80; /* Everforest soft red */
            font-size: 13px;
            margin-top: 12px;
            min-height: 20px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .error-active {
            opacity: 1;
        }
        .input-error input {
            border-color: #e67e80 !important;
            box-shadow: 0 0 0 3px rgba(230, 126, 128, 0.2) !important;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-6px); }
            40%, 80% { transform: translateX(6px); }
        }
        .shake {
            animation: shake 0.4s ease-in-out;
        }

        /* Spinner for loading */
        .spinner {
            display: none;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(20,24,26,0.2);
            border-top: 2px solid #14181a;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .loading button[type="submit"] span {
            display: none;
        }
        .loading button[type="submit"] .spinner {
            display: block;
        }
    </style>
</head>
<body>
    <div class="bg-glow">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
    </div>

    <div class="card-container" id="card-container">
        <div class="card">
            <div class="icon-wrapper">
                <svg class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="url(#lock-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    <defs>
                        <linearGradient id="lock-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#8da874;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#7fbbb3;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            
            <h1>Decryption Required</h1>
            <p>This note is encrypted. Enter the password to unlock it.</p>

            <form id="login-form" onsubmit="handleDecrypt(event)">
                <div class="input-group">
                    <input type="password" id="password-input" placeholder="Enter vault password" required autofocus>
                    <button type="button" class="toggle-password" onclick="togglePasswordVisibility()" aria-label="Toggle Password Visibility">
                        <svg id="eye-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="rgba(211,198,170,0.4)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                    </button>
                </div>
                
                <button type="submit" id="decrypt-btn">
                    <span>Unlock Note</span>
                    <div class="spinner"></div>
                </button>
            </form>

            <div class="error-message" id="error-message"></div>
        </div>
    </div>

    <script>
        // Payload embedded by the encryption script
        const ENCRYPTED_PAYLOAD = "{{ENCRYPTED_PAYLOAD}}";
        const SALT = "{{SALT}}";
        const IV = "{{IV}}";

        function togglePasswordVisibility() {
            const input = document.getElementById('password-input');
            const eyeIcon = document.getElementById('eye-icon');
            if (input.type === 'password') {
                input.type = 'text';
                eyeIcon.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>`;
            } else {
                input.type = 'password';
                eyeIcon.innerHTML = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>`;
            }
        }

        function base64ToBytes(base64) {
            const binString = atob(base64);
            return Uint8Array.from(binString, (m) => m.codePointAt(0));
        }

        function showError(msg) {
            const errEl = document.getElementById('error-message');
            const container = document.getElementById('card-container');
            const inputGroup = document.querySelector('.input-group');
            const input = document.getElementById('password-input');
            
            errEl.textContent = msg;
            errEl.classList.add('error-active');
            inputGroup.classList.add('input-error');
            
            container.classList.remove('shake');
            void container.offsetWidth; // trigger reflow
            container.classList.add('shake');
            
            input.value = '';
            input.focus();
        }

        // Clear error state when user starts typing again
        document.addEventListener('DOMContentLoaded', () => {
            const input = document.getElementById('password-input');
            if (input) {
                input.addEventListener('input', () => {
                    document.getElementById('error-message').classList.remove('error-active');
                    document.querySelector('.input-group').classList.remove('input-error');
                });
            }
        });

        async function decryptContent(password) {
            try {
                const saltBytes = base64ToBytes(SALT);
                const ivBytes = base64ToBytes(IV);
                const ciphertextBytes = base64ToBytes(ENCRYPTED_PAYLOAD);

                const enc = new TextEncoder();
                const baseKey = await window.crypto.subtle.importKey(
                    "raw",
                    enc.encode(password),
                    "PBKDF2",
                    false,
                    ["deriveKey"]
                );

                const key = await window.crypto.subtle.deriveKey(
                    {
                        name: "PBKDF2",
                        salt: saltBytes,
                        iterations: 100000,
                        hash: "SHA-256"
                    },
                    baseKey,
                    { name: "AES-GCM", length: 256 },
                    false,
                    ["decrypt"]
                );

                const decryptedBuffer = await window.crypto.subtle.decrypt(
                    {
                        name: "AES-GCM",
                        iv: ivBytes,
                        tagLength: 128
                    },
                    key,
                    ciphertextBytes
                );

                const dec = new TextDecoder();
                const decryptedHtml = dec.decode(decryptedBuffer);

                // Cache password for session persistence
                sessionStorage.setItem('vault_password', password);

                // Dynamically overwrite document
                document.open();
                document.write(decryptedHtml);
                document.close();
            } catch (e) {
                console.error("Decryption failed:", e);
                showError("Invalid password. Please try again.");
                sessionStorage.removeItem('vault_password');
                document.getElementById('login-form').classList.remove('loading');
                document.getElementById('decrypt-btn').disabled = false;
            }
        }

        async function handleDecrypt(event) {
            event.preventDefault();
            const password = document.getElementById('password-input').value;
            const form = document.getElementById('login-form');
            const btn = document.getElementById('decrypt-btn');
            
            form.classList.add('loading');
            btn.disabled = true;
            document.getElementById('error-message').classList.remove('error-active');

            // Brief timeout to let the spinner render
            setTimeout(() => {
                decryptContent(password);
            }, 150);
        }

        // Auto-decrypt if cached in session
        window.addEventListener('DOMContentLoaded', () => {
            const cachedPassword = sessionStorage.getItem('vault_password');
            if (cachedPassword) {
                document.getElementById('login-form').classList.add('loading');
                document.getElementById('decrypt-btn').disabled = true;
                decryptContent(cachedPassword);
            }
        });
    </script>
</body>
</html>
"""

def is_protected(rel_path):
    path = rel_path.replace("\\\\", "/").replace("\\\\", "/").lower()
    for prefix in PROTECTED_PREFIXES:
        if path.startswith(prefix + "/") or path == prefix or path == prefix + ".html" or path == prefix + "/index.html":
            return True
    return False

def encrypt_file(file_path, password):
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Generate salt and IV
    salt = os.urandom(16)
    iv = os.urandom(12)

    # Derive key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode("utf-8"))

    # Encrypt
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    # Base64 encodings
    b64_payload = base64.b64encode(ciphertext).decode("utf-8")
    b64_salt = base64.b64encode(salt).decode("utf-8")
    b64_iv = base64.b64encode(iv).decode("utf-8")

    # Replace placeholders in HTML template
    encrypted_html = HTML_TEMPLATE.replace("{{ENCRYPTED_PAYLOAD}}", b64_payload)
    encrypted_html = encrypted_html.replace("{{SALT}}", b64_salt)
    encrypted_html = encrypted_html.replace("{{IV}}", b64_iv)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(encrypted_html)

def main():
    if not os.path.exists(PUBLIC_DIR):
        print(f"Error: {PUBLIC_DIR} directory not found. Build the site first.")
        sys.exit(1)

    print(f"Encrypting private content using password from environment...")
    
    count = 0
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, PUBLIC_DIR)
                
                if is_protected(rel_path):
                    print(f"🔒 Encrypting: {rel_path}")
                    encrypt_file(full_path, PASSWORD)
                    count += 1
                    
    print(f"Encryption complete. Encrypted {count} HTML files.")

if __name__ == "__main__":
    main()
