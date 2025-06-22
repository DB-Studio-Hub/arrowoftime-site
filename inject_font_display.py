import os
import re

# Your personal fonts list
personal_fonts = {
    "CormorantGaramond-Regular.ttf": {
        "font_family": "Cormorant Garamond",
        "src": "url('fonts/CormorantGaramond-Regular.ttf') format('truetype')",
        "font_weight": "normal",
        "font_style": "normal"
    },
    "FuturaNowText.ttf": {
        "font_family": "Futura Now Text",
        "src": "url('fonts/FuturaNowText.ttf') format('truetype')",
        "font_weight": "normal",
        "font_style": "normal"
    },
    "neuehaasgrotdisp-25xthin-trial.otf": {
        "font_family": "Neue Haas Grotesk Display Thin",
        "src": "url('fonts/neuehaasgrotdisp-25xthin-trial.otf') format('opentype')",
        "font_weight": "normal",
        "font_style": "normal"
    }
}

def inject_font_display_in_css(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    # Find all @font-face blocks
    font_faces = re.findall(r'@font-face\s*{[^}]*}', css, re.DOTALL)

    modified_css = css
    for block in font_faces:
        # Check if font-display is present
        if 'font-display' not in block:
            # Inject font-display: block; before the closing }
            new_block = block.rstrip('}') + '\n  font-display: block;\n}'
            modified_css = modified_css.replace(block, new_block)

    # Now check for missing personal fonts @font-face
    for file_name, font_data in personal_fonts.items():
        font_family = font_data["font_family"]
        # Check if this font family is already defined in css
        if font_family not in css:
            # Create @font-face block for this font
            font_face_block = f"""
@font-face {{
  font-family: '{font_family}';
  src: {font_data['src']};
  font-weight: {font_data['font_weight']};
  font-style: {font_data['font_style']};
  font-display: block;
}}
"""
            modified_css += font_face_block

    if modified_css != css:
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(modified_css)
        print(f"Injected font-display in {css_path}")
    else:
        print(f"No changes needed in {css_path}")

def inject_google_fonts_in_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Regex to find Google Fonts link href
    pattern = r'(https://fonts\.googleapis\.com/css2\?[^"\']+)'
    matches = re.findall(pattern, html)

    modified_html = html
    for url in matches:
        if 'display=' not in url:
            new_url = url + '&display=block'
            modified_html = modified_html.replace(url, new_url)

    if modified_html != html:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(modified_html)
        print(f"Injected display=block in Google Fonts link in {html_path}")
    else:
        print(f"No Google Fonts changes needed in {html_path}")

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.css'):
                inject_font_display_in_css(path)
            elif file.endswith('.html'):
                inject_google_fonts_in_html(path)

if __name__ == '__main__':
    main()
