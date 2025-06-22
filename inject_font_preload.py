import os

# The preload link tags for your 3 fonts
PRELOAD_LINKS = '''
<link rel="preload" href="fonts/CormorantGaramond-Regular.ttf" as="font" type="font/ttf" crossorigin="anonymous" />
<link rel="preload" href="fonts/FuturaNowText.ttf" as="font" type="font/ttf" crossorigin="anonymous" />
<link rel="preload" href="fonts/neuehaasgrotdisp-25xthin-trial.otf" as="font" type="font/otf" crossorigin="anonymous" />
'''

def inject_preload_in_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '</head>' in content:
        # Insert preload links just before </head>
        content = content.replace('</head>', PRELOAD_LINKS + '\n</head>')
    else:
        print(f"Warning: No </head> tag in {filepath}, skipping preload injection")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Inject preload links in all HTML files
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                inject_preload_in_html(full_path)
                print(f'Injected preload links in {full_path}')

if __name__ == '__main__':
    main()
