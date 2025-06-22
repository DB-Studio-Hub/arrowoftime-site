import os

HEAD_INJECTION = '''
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GB8W0JWL0Y"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GB8W0JWL0Y');
</script>

<!-- Start cookieyes banner -->
<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/9a9a59c61254f1ad3643ddef/script.js"></script>
<!-- End cookieyes banner -->

<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="aot-favicon.ico">
<link rel="apple-touch-icon" href="aot-webclip.png">
'''

FOOTER_INJECTION = '''
<script>
  document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("year").textContent = new Date().getFullYear();
  });
</script>
'''

def inject_code_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '</head>' in content:
        content = content.replace('</head>', HEAD_INJECTION + '\n</head>')
    else:
        print(f'Warning: No </head> tag found in {filepath}, skipping head injection.')

    if '</body>' in content:
        content = content.replace('</body>', FOOTER_INJECTION + '\n</body>')
    else:
        print(f'Warning: No </body> tag found in {filepath}, skipping footer injection.')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                inject_code_in_file(full_path)
                print(f'Injected code in {full_path}')

if __name__ == '__main__':
    main()
