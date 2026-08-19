#!/usr/bin/python3

templateHTML = """
    
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">
    <title>Password Protected Page</title>
    <style>
        html, body {
            margin: 0;
            width: 100%;
            height: 100%;
            font-family: Arial, Helvetica, sans-serif;
        }
        #dialogText {
            color: white;
            background-color: #333333;
        }
        
        #dialogWrap {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: table;
            background-color: #EEEEEE;
        }
        
        #dialogWrapCell {
            display: table-cell;
            text-align: center;
            vertical-align: middle;
        }
        
        #mainDialog {
            max-width: 400px;
            margin: 5px;
            border: solid #AAAAAA 1px;
            border-radius: 10px;
            box-shadow: 3px 3px 5px 3px #AAAAAA;
            margin-left: auto;
            margin-right: auto;
            background-color: #FFFFFF;
            overflow: hidden;
            text-align: left;
        }
        #mainDialog > * {
            padding: 10px 30px;
        }
        #passArea {
            padding: 20px 30px;
            background-color: white;
        }
        #passArea > * {
            margin: 5px auto;
        }
        #pass {
            width: 100%;
            height: 40px;
            font-size: 30px;
        }
        
        #messageWrapper {
            float: left;
            vertical-align: middle;
            line-height: 30px;
        }
        
        .notifyText {
            display: none;
        }
        
        #invalidPass {
            color: red;
        }
        
        #success {
            color: green;
        }
        
        #submitPass {
            font-size: 20px;
            border-radius: 5px;
            background-color: #E7E7E7;
            border: solid gray 1px;
            float: right;
            cursor: pointer;
        }
        #contentFrame {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        #attribution {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            font-size: 0.8em;
        }
        #attribution, #attribution a {
            color: #999;
        }
        .error {
            display: none;
            color: red;
        }
    </style>
  </head>
  <body>
    <iframe id="contentFrame" frameBorder="0" allowfullscreen></iframe>
    <div id="dialogWrap">
        <div id="dialogWrapCell">
            <div id="mainDialog">
                <div id="dialogText">Password protected</div>
                <div id="passArea">
                    <p id="passwordPrompt">Password</p>
                    <input id="pass" type="password" name="pass" autofocus>
                    <div>
                        <span id="messageWrapper">
                            <span id="invalidPass" class="error">Sorry, please try again.</span>
                            <span id="trycatcherror" class="error">Sorry, something went wrong.</span>
                            <span id="success" class="notifyText">Success!</span>
                            &nbsp;
                        </span>
                        <button id="submitPass" type="button">Submit</button>
                        <div style="clear: both;"></div>
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
            </div>
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


try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("install cryptography: \"pip3 install cryptography\"")
    exit(1)
import os, re
from base64 import b64encode
from getpass import getpass
import codecs


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
    encryptedDocument = templateHTML.replace('Password Protected Page', title).replace("/*{{ENCRYPTED_PAYLOAD}}*/\"\"", encryptedPl)

    # filename, extension = os.path.splitext(inputfile)
    # outputfile = filename + "-protected" + extension
    outputfile = inputfile
    with codecs.open(outputfile, 'w','utf-8-sig') as f:
        f.write(encryptedDocument)
    print("File saved to %s"%outputfile)

if __name__ == "__main__":

    import argparse
    from pathlib import Path

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