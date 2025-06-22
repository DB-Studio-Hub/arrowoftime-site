import os
import re

def remove_webflow_badge_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove elements with class "w-webflow-badge"
    new_content = re.sub(
        r'<[^>]*class="[^"]*w-webflow-badge[^"]*"[^>]*>.*?</[^>]+>',
        '',
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Removed Webflow badge from {filepath}")

def main():
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                remove_webflow_badge_from_file(full_path)

if __name__ == '__main__':
    main()
