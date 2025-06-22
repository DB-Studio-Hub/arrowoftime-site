import os

FONT_DISPLAY_CSS = '''
<style>
@font-face {
  font-display: swap;
}
</style>
'''

def inject_font_css(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '</head>' in content:
        content = content.replace('</head>', FONT_DISPLAY_CSS + '\n</head>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Injected font-display CSS in {filepath}')
    else:
        print(f'Warning: No </head> tag found in {filepath}, skipping font CSS injection.')

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                inject_font_css(full_path)

if __name__ == '__main__':
    main()
