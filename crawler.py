#!/usr/bin/env python3
"""
Web Crawler for Website Archival
Downloads a website recursively, fixes URLs, and prepares for GitHub Pages
"""

import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import html
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, base_url, output_dir, max_pages=200):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_pages = max_pages
        self.downloaded_urls = set()
        self.all_pages = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def normalize_url(self, url):
        """Normalize URL to avoid duplicates"""
        if not url:
            return None
        url = urljoin(self.base_url, url)
        # Parse and remove fragments
        parsed = urlparse(url)
        if parsed.netloc != self.domain:
            return None
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}" + (f"?{parsed.query}" if parsed.query else "")

    def get_filename(self, url):
        """Convert URL to filename"""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path or path.endswith('/'):
            path = path.rstrip('/') + '/index'
        
        filename = path.replace('/', '_')
        if parsed.query:
            filename += '_' + parsed.query.replace('=', '-').replace('&', '_')
        
        if not filename.endswith('.html'):
            filename += '.html'
        
        return filename

    def download_url(self, url):
        """Download a single URL"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return None

    def fix_urls_in_html(self, html_content, original_url):
        """Fix URLs in HTML to point to local files"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Fix links
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            normalized = self.normalize_url(href)
            if normalized:
                # Convert to relative path in pages folder
                filename = self.get_filename(normalized)
                tag['href'] = f"../pages/{filename}"
            elif href.startswith('#'):
                pass  # Keep anchors as is
            else:
                tag['href'] = href  # Keep external links
        
        # Fix images
        for tag in soup.find_all('img', src=True):
            src = tag['src']
            abs_url = urljoin(original_url, src)
            # For now, keep external image sources (could download if needed)
        
        return str(soup.prettify())

    def crawl(self):
        """Start crawling from base URL"""
        logger.info(f"Starting crawl of {self.base_url}")
        to_visit = [self.base_url]
        visited_urls = set()
        
        while to_visit and len(visited_urls) < self.max_pages:
            url = to_visit.pop(0)
            if url in visited_urls:
                continue
            
            visited_urls.add(url)
            logger.info(f"Downloading ({len(visited_urls)}/{self.max_pages}): {url}")
            
            html_content = self.download_url(url)
            if not html_content:
                continue
            
            # Extract links for further crawling
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                normalized = self.normalize_url(href)
                if normalized and normalized not in visited_urls:
                    to_visit.append(normalized)
            
            # Fix URLs and save
            fixed_html = self.fix_urls_in_html(html_content, url)
            filename = self.get_filename(url)
            filepath = self.output_dir / 'pages' / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_html)
            
            self.all_pages.append({
                'url': url,
                'filename': filename,
                'title': soup.title.string if soup.title else url
            })
        
        logger.info(f"\nCrawl complete! Downloaded {len(self.all_pages)} pages")
        return self.all_pages

    def generate_index(self):
        """Generate index.html with all pages"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archived: {self.domain}</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }}
        .stats {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .pages-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        .page-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
            text-decoration: none;
            color: #333;
        }}
        .page-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            background: #e9ecef;
        }}
        .page-card h3 {{
            color: #667eea;
            margin-bottom: 8px;
            font-size: 16px;
            word-break: break-word;
        }}
        .page-card p {{
            font-size: 12px;
            color: #999;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 Archived: {self.domain}</h1>
        <div class="stats">
            <p><strong>{len(self.all_pages)}</strong> pages archived</p>
        </div>
        <div class="pages-grid">
"""
        
        for page in self.all_pages:
            title = page['title'][:50] if page['title'] else page['url']
            html += f"""            <a href="pages/{page['filename']}" class="page-card">
                <h3>🔗 {html.escape(title)}</h3>
                <p>{html.escape(page['url'][:80])}</p>
            </a>
"""
        
        html += """        </div>
    </div>
</body>
</html>"""
        
        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Generated index.html")

if __name__ == '__main__':
    BASE_URL = 'https://callmedley.com'
    OUTPUT_DIR = 'sites/callmedley_com'
    
    crawler = WebCrawler(BASE_URL, OUTPUT_DIR, max_pages=100)
    crawler.crawl()
    crawler.generate_index()
    logger.info("Done!")
