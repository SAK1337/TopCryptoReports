import os
from bs4 import BeautifulSoup
import re

# --- CONFIGURATION ---
CURRENT_DATE = "13-11-2025"
WEBSITE_DIR = f"website-{CURRENT_DATE}"

# --- SCRIPT ---

def validate_and_fix_html(filepath):
    """Validates and fixes common HTML issues in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix invalid tag nesting: <p><h3>...</h3></p> -> <h3>...</h3>
    content = re.sub(r'<p>\s*<h3>(.*?)</h3>\s*</p>', r'<h3>\1</h3>', content)
    
    # Use BeautifulSoup for more complex validation if needed
    soup = BeautifulSoup(content, 'html.parser')
    
    # Example: Check for broken back-link
    back_link = soup.find('a', class_='back-link')
    if back_link and not os.path.exists(os.path.join(os.path.dirname(filepath), back_link['href'])):
        print(f"  - WARNING: Broken back-link in {os.path.basename(filepath)}: {back_link['href']}")

    # Check for CSS file reference
    css_link = soup.find('link', rel='stylesheet')
    if css_link:
        css_path = os.path.join(os.path.dirname(filepath), css_link['href'])
        if not os.path.exists(css_path):
            print(f"  - WARNING: CSS file not found for {os.path.basename(filepath)}: {css_link['href']}")
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_validation():
    """Runs the validation process for the entire website."""
    print(f"\n🔍 VALIDATING HTML for {WEBSITE_DIR}")
    if not os.path.exists(WEBSITE_DIR):
        print(f"Error: Website directory not found at '{WEBSITE_DIR}'")
        return

    fixed_files_count = 0
    total_files_scanned = 0

    # Scan root directory
    for filename in os.listdir(WEBSITE_DIR):
        if filename.endswith('.html'):
            total_files_scanned += 1
            if validate_and_fix_html(os.path.join(WEBSITE_DIR, filename)):
                fixed_files_count += 1
                print(f"  - Fixed issues in {filename}")

    # Scan main directory
    main_dir = os.path.join(WEBSITE_DIR, 'main')
    if os.path.exists(main_dir):
        for filename in os.listdir(main_dir):
            if filename.endswith('.html'):
                total_files_scanned += 1
                if validate_and_fix_html(os.path.join(main_dir, filename)):
                    fixed_files_count += 1
                    print(f"  - Fixed issues in main/{filename}")
    
    print("\n✅ HTML VALIDATION COMPLETE")
    print(f"📊 Files scanned: {total_files_scanned}")
    print(f"🛠️ Files fixed: {fixed_files_count}")

if __name__ == "__main__":
    run_validation()
