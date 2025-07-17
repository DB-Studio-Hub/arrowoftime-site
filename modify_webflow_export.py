import os
import datetime
import re

# --- Injection code ---
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

    # Inject head code
    if '</head>' in content:
        content = content.replace('</head>', HEAD_INJECTION + '\n</head>')
    else:
        print(f'Warning: No </head> tag found in {filepath}, skipping head injection.')

    # Inject footer code
    if '</body>' in content:
        content = content.replace('</body>', FOOTER_INJECTION + '\n</body>')
    else:
        print(f'Warning: No </body> tag found in {filepath}, skipping footer injection.')

    # Remove Webflow badge(s)
    new_content = re.sub(
        r'<[^>]*class="[^"]*w-webflow-badge[^"]*"[^>]*>.*?</[^>]+>',
        '',
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        content = new_content
        print(f'Removed Webflow badge from {filepath}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Injected code in {filepath}')

# --- Sitemap generation ---
def generate_sitemap(domain, output='sitemap.xml'):
    html_urls = []
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.html'):
                rel_path = os.path.join(root, name).replace('./', '').replace('\\', '/')
                url_path = '/' + rel_path
                full_url = domain + url_path
                html_urls.append(full_url)

    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for url in html_urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{url}</loc>')
        lines.append(f'    <lastmod>{now}</lastmod>')
        lines.append('  </url>')

    lines.append('</urlset>')

    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Sitemap generated with {len(html_urls)} URLs → {output}')

# --- Main function ---
def main():
    print("Starting injection and cleanup...")

    # Inject code and remove badges
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                inject_code_in_file(filepath)

    print("Injection and cleanup complete.\n")

    # Generate sitemap
    domain = 'https://arrowoftime.net'  # Update if your domain changes
    generate_sitemap(domain)

if __name__ == '__main__':
    main()
