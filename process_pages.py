#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def main():
    # Read all HTML files from the find command output
    all_files = []
    if os.path.exists('/tmp/all_files.txt'):
        with open('/tmp/all_files.txt', 'r') as f:
            all_files = [line.strip() for line in f.readlines() if line.strip()]
    
    if not all_files:
        print("ERROR: No files found in /tmp/all_files.txt")
        return 1
    
    print(f"Found {len(all_files)} HTML files")
    
    # Create pages directory
    pages_dir = Path('sites/callmedley_com/pages')
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    # Process files
    page_mapping = []
    for idx, file_path in enumerate(all_files[:200], 1):
        target_name = f'page-{idx}.html'
        target_path = pages_dir / target_name
        
        try:
            shutil.copy2(file_path, target_path)
            # Generate URL-like format
            url_like = 'https://callmedley.com/' + file_path.replace('sites/callmedley_com/', '').replace('index.html', '').rstrip('/')
            page_mapping.append((target_name, url_like))
        except Exception as e:
            print(f"Error copying {file_path}: {e}")
    
    print(f"Copied {len(page_mapping)} files")
    
    # Generate index.html
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>callmedley_com</title>',
        '<style>',
        '* { margin: 0; padding: 0; }',
        'body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f5f5f5; padding: 20px; }',
        '.container { max-width: 1000px; margin: 0 auto; }',
        'h1 { color: #333; margin-bottom: 30px; }',
        '.page-list { list-style: none; }',
        '.page-item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 6px; border-left: 4px solid #667eea; }',
        'a { color: #667eea; text-decoration: none; }',
        'a:hover { text-decoration: underline; }',
        '</style>',
        '</head>',
        '<body>',
        '<div class="container">',
        f'<h1>📄 callmedley_com ({len(page_mapping)} pages)</h1>',
        '<ul class="page-list">'
    ]
    
    for page_file, url in page_mapping:
        html_lines.append(f'<li class="page-item"><a href="{page_file}">🔗 {url}</a></li>')
    
    html_lines.extend([
        '</ul>',
        '</div>',
        '</body>',
        '</html>'
    ])
    
    # Write index.html
    index_path = Path('sites/callmedley_com/index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    
    print(f"Generated index.html with {len(page_mapping)} pages")
    return 0

if __name__ == '__main__':
    exit(main())
