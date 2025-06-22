import os
import re

# Your 3 font names, matching the font-family names in your CSS @font-face rules
FONT_NAMES = [
    'CormorantGaramond-Regular',
    'FuturaNowText',
    'neuehaasgrotdisp-25xthin-trial'
]

def update_font_display(css_text):
    # Pattern to find @font-face blocks for your fonts
    def replace_font_display(match):
        block = match.group(0)
        # If font-display exists, replace it
        if 'font-display' in block:
            block = re.sub(r'font-display\s*:\s*\w+;', 'font-display: block;', block)
        else:
            # Insert font-display: block; before the closing }
            block = block.rstrip('}') + '\n  font-display: block;\n}'
        return block

    for font_name in FONT_NAMES:
        # Regex to find the font-face block for that font-family
        pattern = re.compile(
            r'@font-face\s*{[^}]*font-family\s*:\s*[\'"]?' + re.escape(font_name) + r'[\'"]?;[^}]*}',
            re.IGNORECASE | re.DOTALL
        )
        css_text = pattern.sub(replace_font_display, css_text)

    return css_text

def process_css_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        css_content = f.read()

    updated_css = update_font_display(css_content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_css)
    print(f'Injected font-display block in {filepath}')

def main():
    # Process all .css files in current folder recursively
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.css'):
                full_path = os.path.join(root, file)
                process_css_file(full_path)

if __name__ == '__main__':
    main()
