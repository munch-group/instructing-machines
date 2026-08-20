#!/usr/bin/python3

templateHTML = """
    
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">
    <title>Password Protected Page</title>
    <link rel="preconnect" href="https://rsms.me">
    <link rel="stylesheet" href="https://rsms.me/inter/inter.css">
    <style>
        /* The gate borrows the book's own tokens: teal primary, Inter body
           text, thin grey rules, 4px corners.  Kept in sync by hand with
           docs/custom.scss -- there is no build step that could share them. */
        :root {
            --im-primary:      #0D7D92;
            --im-primary-dark: #0B6576;
            --im-caret:        #7C5CB0;
            --im-ink:          #151617;
            --im-body:         #343a40;
            --im-muted:        #495057;
            --im-quiet:        #6c757d;
            --im-rule:         #D1D5DB;
            --im-danger:       #ff0039;
            --im-success:      #3fb618;
            --im-sans: "Inter var", "Inter", -apple-system, BlinkMacSystemFont,
                       "Segoe UI", Helvetica, Arial, sans-serif;
            --im-mono: "Fira Code", "DejaVu Sans Mono", ui-monospace,
                       SFMono-Regular, Menlo, monospace;
        }

        html, body {
            margin: 0;
            width: 100%;
            height: 100%;
        }
        body {
            font-family: var(--im-sans);
            font-size: 16px;
            line-height: 1.5;
            color: var(--im-body);
            background-color: #ffffff;
            -webkit-font-smoothing: antialiased;
        }

        #contentFrame {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }

        #dialogWrap {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            overflow-y: auto;
            background-color: #ffffff;
        }
        #dialogWrapCell {
            margin: auto;
            width: 100%;
            max-width: 34rem;
            padding: 2.5rem 1.5rem 3rem;
            box-sizing: border-box;
        }

        /* --- header: the prompt lockup, as on the landing page --- */

        .im-header {
            text-align: center;
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--im-rule);
        }
        @media (min-resolution: 2dppx) {
            .im-header { border-bottom-width: 0.5px; }
        }
        .im-header svg {
            display: inline-block;
            width: 100%;
            max-width: 22rem;
            height: auto;
        }
        /* only rendered if the wordmark file has moved */
        .im-logo-text {
            display: inline-block;
            font-family: var(--im-mono);
            font-size: clamp(1.05rem, 4.5vw, 1.6rem);
            font-weight: 500;
            color: var(--im-ink);
            white-space: nowrap;
        }
        .im-logo-chevron { color: var(--im-primary); }
        .im-logo-caret   { color: var(--im-caret); }

        /* --- the ask --- */

        .im-eyebrow {
            display: block;
            font-family: var(--im-mono);
            font-size: 0.78rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--im-primary);
            margin-bottom: 0.625rem;
        }
        .im-title {
            font-size: 1.6rem;
            line-height: 1.2;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--im-ink);
            margin: 0 0 0.75rem;
        }
        .im-lede {
            font-size: 1rem;
            line-height: 1.55;
            color: var(--im-muted);
            margin: 0 0 1.75rem;
        }

        /* --- the form --- */

        .im-label {
            display: block;
            font-size: 0.84rem;
            font-weight: 500;
            color: var(--im-ink);
            margin-bottom: 0.4rem;
        }
        #pass {
            display: block;
            width: 100%;
            box-sizing: border-box;
            font-family: inherit;
            font-size: 1rem;
            color: var(--im-ink);
            padding: 0.65rem 0.75rem;
            background-color: #ffffff;
            border: 1px solid var(--im-rule);
            border-radius: 4px;
            outline: none;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }
        #pass:focus {
            border-color: var(--im-primary);
            box-shadow: 0 0 0 3px rgba(13, 125, 146, 0.15);
        }
        #pass:disabled {
            background-color: #f8f9fa;
            color: var(--im-quiet);
        }

        .im-actions {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.875rem;
            margin-top: 1rem;
            min-height: 2.6rem;
        }
        #submitPass {
            font-family: inherit;
            font-size: 0.97rem;
            font-weight: 500;
            padding: 0.65rem 1.2rem;
            border-radius: 4px;
            color: #ffffff;
            background-color: var(--im-primary);
            border: 1px solid var(--im-primary);
            cursor: pointer;
            white-space: nowrap;
            transition: background-color 0.15s ease, border-color 0.15s ease;
        }
        #submitPass:hover:enabled {
            background-color: var(--im-primary-dark);
            border-color: var(--im-primary-dark);
        }
        #submitPass:focus-visible {
            outline: 2px solid var(--im-primary);
            outline-offset: 2px;
        }
        #submitPass:disabled {
            opacity: 0.55;
            cursor: default;
        }

        #messageWrapper {
            font-size: 0.9rem;
        }
        .notifyText { display: none; }
        .error      { display: none; }
        #invalidPass, #trycatcherror { color: var(--im-danger); }
        #success                     { color: var(--im-success); }

        /* The two browser-capability notices replace the form entirely, so the
           line telling the reader to type a password would be left pointing at
           nothing.  Browsers without :has() just keep it, as before. */
        #mainDialog:has(#passArea[style*="none"]) .im-lede { display: none; }

        #securecontext, #nocrypto {
            border: 1px solid var(--im-rule);
            border-left: 3px solid var(--im-danger);
            border-radius: 4px;
            padding: 0.25rem 1rem;
        }
        #securecontext p, #nocrypto p {
            font-size: 0.95rem;
            line-height: 1.55;
        }

        /* --- footer --- */

        .im-footer {
            margin-top: 2.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--im-rule);
            font-size: 0.8rem;
            color: var(--im-quiet);
        }
        @media (min-resolution: 2dppx) {
            .im-footer { border-top-width: 0.5px; }
        }

        @media (prefers-reduced-motion: reduce) {
            #pass, #submitPass { transition: none; }
        }
    </style>
  </head>
  <body>
    <iframe id="contentFrame" frameBorder="0" allowfullscreen></iframe>
    <div id="dialogWrap">
        <div id="dialogWrapCell">
            <header class="im-header"><!--{{LOGO}}--></header>
            <main id="mainDialog">
                <span class="im-eyebrow">Protected page</span>
                <h1 id="dialogText" class="im-title">Password required</h1>
                <p class="im-lede">This page is not public. Enter the password to open it.</p>
                <div id="passArea">
                    <label id="passwordPrompt" class="im-label" for="pass">Password</label>
                    <input id="pass" type="password" name="pass" autocomplete="current-password" autofocus>
                    <div class="im-actions">
                        <button id="submitPass" type="button">Submit</button>
                        <span id="messageWrapper" aria-live="polite">
                            <span id="invalidPass" class="error">Sorry, please try again.</span>
                            <span id="trycatcherror" class="error">Sorry, something went wrong.</span>
                            <span id="success" class="notifyText">Success!</span>
                        </span>
                    </div>
                </div>
                <div id="securecontext" class="error">
                    <p>
                        Sorry, but password protection only works over a secure connection. Please load this page via HTTPS.
                    </p>
                </div>
                <div id="nocrypto" class="error">
                    <p>
                        Your web browser appears to be outdated. Please visit this page using a modern browser.
                    </p>
                </div>
            </main>
            <footer class="im-footer">Kasper Munch &middot; Bioinformatics Research Centre, Aarhus University</footer>
        </div>
    </div>
    <script>
    (function() {

        var pl = /*{{ENCRYPTED_PAYLOAD}}*/"";
        
        var submitPass = document.getElementById('submitPass');
        var passEl = document.getElementById('pass');
        var invalidPassEl = document.getElementById('invalidPass');
        var trycatcherror = document.getElementById('trycatcherror');
        var successEl = document.getElementById('success');
        var contentFrame = document.getElementById('contentFrame');
        
        // Sanity checks

        if (pl === "") {
            submitPass.disabled = true;
            passEl.disabled = true;
            alert("This page is meant to be used with the encryption tool. It doesn't work standalone.");
            return;
        }

        if (!isSecureContext) {
            document.querySelector("#passArea").style.display = "none";
            document.querySelector("#securecontext").style.display = "block";
            return;
        }

        if (!crypto.subtle) {
            document.querySelector("#passArea").style.display = "none";
            document.querySelector("#nocrypto").style.display = "block";
            return;
        }
        
        function str2ab(str) {
            var ustr = atob(str);
            var buf = new ArrayBuffer(ustr.length);
            var bufView = new Uint8Array(buf);
            for (var i=0, strLen=ustr.length; i < strLen; i++) {
                bufView[i] = ustr.charCodeAt(i);
            }
            return bufView;
        }

        async function deriveKey(salt, password) {
            const encoder = new TextEncoder()
            const baseKey = await crypto.subtle.importKey(
                'raw',
                encoder.encode(password),
                'PBKDF2',
                false,
                ['deriveKey'],
            )
            return await crypto.subtle.deriveKey(
                { name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' },
                baseKey,
                { name: 'AES-GCM', length: 256 },
                true,
                ['decrypt'],
            )
        }
        
        async function doSubmit(evt) {
            submitPass.disabled = true;
            passEl.disabled = true;

            let iv, ciphertext, key;
            
            try {
                var unencodedPl = str2ab(pl);

                const salt = unencodedPl.slice(0, 32)
                iv = unencodedPl.slice(32, 32 + 16)
                ciphertext = unencodedPl.slice(32 + 16)

                key = await deriveKey(salt, passEl.value);
            } catch (e) {
                trycatcherror.style.display = "inline";
                console.error(e);
                return;
            }

            try {
                const decryptedArray = new Uint8Array(
                    await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ciphertext)
                );

                let decrypted = new TextDecoder().decode(decryptedArray);

                if (decrypted === "") throw "No data returned";

                const basestr = '<base href="." target="_top">';
                const anchorfixstr = `
                    <script>
                        Array.from(document.links).forEach((anchor) => {
                            const href = anchor.getAttribute("href");
                            if (href.startsWith("#")) {
                                anchor.addEventListener("click", function(e) {
                                    e.preventDefault();
                                    const targetId = this.getAttribute("href").substring(1);
                                    const targetEl = document.getElementById(targetId);
                                    targetEl.scrollIntoView();
                                });
                            }
                        });
                    <\\/script>
                `;
                
                // Set default iframe link targets to _top so all links break out of the iframe
                if (decrypted.includes("<head>")) decrypted = decrypted.replace("<head>", "<head>" + basestr);
                else if (decrypted.includes("<!DOCTYPE html>")) decrypted = decrypted.replace("<!DOCTYPE html>", "<!DOCTYPE html>" + basestr);
                else decrypted = basestr + decrypted;

                // Fix fragment links
                if (decrypted.includes("</body>")) decrypted = decrypted.replace("</body>", anchorfixstr + '</body>');
                else if (decrypted.includes("</html>")) decrypted = decrypted.replace("</html>", anchorfixstr + '</html>');
                else decrypted = decrypted + anchorfixstr;
                
                contentFrame.srcdoc = decrypted;
                
                successEl.style.display = "inline";
                setTimeout(function() {
                    dialogWrap.style.display = "none";
                }, 1000);
            } catch (e) {
                invalidPassEl.style.display = "inline";
                passEl.value = "";
                submitPass.disabled = false;
                passEl.disabled = false;
                console.error(e);
                return;
            }
        }
        
        submitPass.onclick = doSubmit;
        passEl.onkeypress = function(e){
            if (!e) e = window.event;
            var keyCode = e.keyCode || e.which;
            invalidPassEl.style.display = "none";
            if (keyCode == '13'){
              // Enter pressed
              doSubmit();
              return false;
            }
        }
    })();
    </script>
  </body>
</html>	
    
"""



from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os, re
from base64 import b64encode
from functools import lru_cache
from getpass import getpass
from pathlib import Path
import codecs


WORDMARK = Path(__file__).resolve().parent.parent / 'docs' / 'logo' / 'im-prompt.svg'


@lru_cache(maxsize=1)
def wordmark_markup():
    """The site's prompt lockup, inlined so the gate needs no separate asset.

    The page can be served from any depth under the output directory, so a
    relative <img src> would have to be recomputed per file; the SVG is small
    next to the encrypted payload, so it goes in whole.  If the file has moved
    (build_logo.py writes it), fall back to a text lockup in the same colors.
    """
    try:
        svg = WORDMARK.read_text(encoding='utf-8')
    except OSError:
        return ('<span class="im-logo-text">'
                '<span class="im-logo-chevron">&gt;</span>&nbsp;instructing machines'
                '<span class="im-logo-caret">&#9612;</span></span>')
    return re.sub(r'^\s*<\?xml.*?\?>\s*', '', svg, flags=re.S).strip()


# def main():
# 	# sanitize input
# 	if len(sys.argv) < 2:
# 		print("Usage:\n%s filename [passphrase]"%sys.argv[0])
# 		exit(0)
        
def encrypt_file(inputfile, passphrase):        
    # inputfile = sys.argv[1]
    try:
        with open(inputfile, "rb") as f:
            data = f.read()
    except:
        print("Cannot open file: %s"%inputfile)
        exit(1)

    title = re.search(r'<title.*?>(.+?)</title>', data.decode()).group(1)

    salt = os.urandom(32)
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    ).derive(passphrase.encode('utf-8'))
    iv = os.urandom(16)

    # encrypt() appends the 16-byte GCM tag to the ciphertext
    encrypted = AESGCM(key).encrypt(iv, data, None)

    # projectFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # with open(os.path.join(projectFolder, "decryptTemplate.html")) as f:
    # 	templateHTML = f.read()

    encryptedPl = f'"{b64encode(salt+iv+encrypted).decode("utf-8")}"'
    # encryptedDocument = templateHTML.replace("/*{{ENCRYPTED_PAYLOAD}}*/\"\"", encryptedPl)
    encryptedDocument = (templateHTML
                         .replace('Password Protected Page', title)
                         .replace('<!--{{LOGO}}-->', wordmark_markup())
                         .replace('/*{{ENCRYPTED_PAYLOAD}}*/""', encryptedPl))

    # filename, extension = os.path.splitext(inputfile)
    # outputfile = filename + "-protected" + extension
    outputfile = inputfile
    with codecs.open(outputfile, 'w','utf-8-sig') as f:
        f.write(encryptedDocument)
    print("File saved to %s"%outputfile)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')

    parser.add_argument('-p', '--passphrase') 
    parser.add_argument('input_file_names', nargs='*', type=Path) 
    
    args = parser.parse_args()

    if args.passphrase:
        passphrase = args.passphrase
    else:
        while True:
            passphrase = getpass(prompt='Password: ')
            if passphrase == getpass(prompt='Confirm: '):
                break
            print("Passwords don\'t match, try again.")

    for p in args.input_file_names:

        if p.is_dir():
            for file_name in p.glob('**/*.html'):
                encrypt_file(file_name, passphrase)
        else:
            file_name = p
            encrypt_file(file_name, passphrase)

        


# if __name__ == "__main__":
# 	main()