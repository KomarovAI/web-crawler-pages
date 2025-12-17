#!/usr/bin/env python3
import os
import glob
import shutil
from pathlib import Path
from urllib.parse import quote

def main():
    # Find all HTML files directly
    base_dir = Path('sites/callmedley_com')
    html_files = sorted(glob.glob(str(base_dir / '**' / '*.html'), recursive=True))
    
    # Filter to exclude the index.html we'll be creating
    html_files = [f for f in html_files if not f.endswith('sites/callmedley_com/pages/index.html')]
    
    if not html_files:
        print("ERROR: No HTML files found to process")
        return 1
    
    print(f"Found {len(html_files)} HTML files")
    
    # Create pages directory
    pages_dir = base_dir / 'pages'
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    # Process and copy files
    page_mapping = []
    for idx, file_path in enumerate(html_files[:200], 1):
        target_name = f'page-{idx}.html'
        target_path = pages_dir / target_name
        
        try:
            shutil.copy2(file_path, target_path)
            # Convert file path to URL-like format for display
            rel_path = file_path.replace(str(base_dir) + '/', '')
            url_like = 'https://callmedley.com/' + rel_path.replace('index.html', '').rstrip('/')
            page_mapping.append((target_name, url_like))
            print(f"Copied {idx}: {target_name} <- {rel_path}")
        except Exception as e:
            print(f"Error copying {file_path}: {e}")
    
    print(f"\nSuccessfully copied {len(page_mapping)} files")
    
    # Generate index.html in main callmedley_com directory
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>callmedley_com - ' + str(len(page_mapping)) + ' pages</title>',
        '<style>',
        '* { margin: 0; padding: 0; }',
        'body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }',
        '.container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 8px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }',
        'h1 { color: #333; margin-bottom: 30px; text-align: center; }',
        '.page-list { list-style: none; display: grid; gap: 10px; }',
        '.page-item { background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #667eea; transition: all 0.3s; }',
        '.page-item:hover { background: #e9ecef; transform: translateX(5px); }',
        'a { color: #667eea; text-decoration: none; font-weight: 500; }',
        'a:hover { text-decoration: underline; }',
        '.stats { background: #e9ecef; padding: 20px; border-radius: 6px; margin-bottom: 30px; text-align: center; }',
        '.stats p { margin: 5px 0; color: #666; }',
        '</style>',
        '</head>',
        '<body>',
        '<div class="container">',
        f'<h1>📄 callmedley.com - {len(page_mapping)} pages archived</h1>',
        '<div class="stats">',
        f'<p><strong>Total pages:</strong> {len(page_mapping)}</p>',
        '<p>Crawled and archived with web-crawler-pages</p>',
        '</div>',
        '<ul class="page-list">'
    ]
    
    for page_file, url in page_mapping:
        html_lines.append(f'<li class="page-item"><a href="pages/{page_file}">🔗 {url}</a></li>')
    
    html_lines.extend([
        '</ul>',
        '</div>',
        '</body>',
        '</html>'
    ])
    
    # Write main index.html
    index_path = base_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    
    print(f"\nGenerated main index.html with {len(page_mapping)} page links")
    return 0

if __name__ == '__main__':
    exit(main())
