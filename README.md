# 🌐 Web Crawler Pages - GitHub Pages Deployment

Automatically deploy crawled websites to GitHub Pages from the [web-crawler](https://github.com/KomarovAI/web-crawler) repository.

## 🚀 How to Use

### Option 1: Manual Trigger

1. Go to **Actions** → **🌐 Deploy Crawled Sites to GitHub Pages**
2. Click **Run workflow**
3. Fill in the inputs:
   - **source_repo**: `KomarovAI/web-crawler` (or your fork)
   - **run_id**: Get from https://github.com/KomarovAI/web-crawler/actions (click on a run)
   - **site_domain**: e.g., `callmedley-com`
4. Click **Run workflow**

### Option 2: From Command Line

After running the crawler:

```bash
# Trigger deployment
gh workflow run deploy.yml -R KomarovAI/web-crawler-pages \
  -f source_repo=KomarovAI/web-crawler \
  -f run_id=20216321056 \
  -f site_domain=callmedley-com
```

## 📊 What It Does

```
┌──────────────────────────────┐
│  web-crawler artifacts       │
│  (SQLite databases)          │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│  web-crawler-pages deploy    │
│  1. Download artifacts       │
│  2. Extract databases        │
│  3. Generate HTML pages      │
│  4. Deploy to GitHub Pages   │
└──────────────┬───────────────┘
               │
               ↓
     🌐 GitHub Pages Site
     (live and searchable)
```

## 🎯 Features

✅ **Automatic Deployment**
- Downloads artifacts from web-crawler runs
- Extracts SQLite databases
- Generates searchable HTML pages
- Deploys to GitHub Pages automatically

✅ **Beautiful UI**
- Card-based layout for site overview
- Gradient design with responsive layout
- Direct links to view crawled pages
- Statistics (page count, DB size)

✅ **Fast Access**
- All pages indexed and searchable
- Quick navigation between pages
- Lightweight HTML files

## 📝 Structure

```
.
├── index.html                    # Main archive page
├── sites/
│   ├── callmedley_com/          # Site 1
│   │   ├── index.html           # Site index
│   │   ├── callmedley_com.db    # SQLite database
│   │   └── pages/
│   │       ├── page-1.html
│   │       ├── page-2.html
│   │       └── ...
│   ├── another-domain_com/      # Site 2
│   │   └── ...
│   └── ...
└── .github/
    └── workflows/
        └── deploy.yml
```

## ⚙️ Workflow Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `source_repo` | `KomarovAI/web-crawler` | Source repository (owner/repo) |
| `run_id` | - | Workflow run ID to download artifacts from |
| `site_domain` | `callmedley-com` | Domain name for folder creation |

## 📖 Example

**Scenario**: You crawled `https://callmedley.com` with the crawler and got run ID `20216321056`.

1. Trigger deployment:
   ```bash
   gh workflow run deploy.yml \
     -f source_repo=KomarovAI/web-crawler \
     -f run_id=20216321056 \
     -f site_domain=callmedley-com
   ```
2. Wait 2-5 minutes
3. Visit your GitHub Pages URL: `https://komarovai.github.io/web-crawler-pages/`
4. See your crawled site with all pages!

## 🌐 GitHub Pages Setup

Pages are automatically deployed to:
```
https://<your-username>.github.io/web-crawler-pages/
```

To verify it's working:
1. Go to **Settings** → **Pages**
2. You should see: "Your site is live at https://..."

## 🔒 Permissions

This workflow needs:
- ✅ `contents: write` - Push to main branch
- ✅ `pages: write` - Deploy to GitHub Pages
- ✅ `id-token: write` - OIDC for Pages deployment

## 📊 What Gets Generated

### Main Index Page
- Card for each crawled site
- Shows: Page count, DB size, original URL
- Direct link to view site

### Per-Site Index
- List of all crawled pages
- Link to each page
- Page count

### Individual Page Files
- Page HTML with title
- Original URL preserved
- Navigation back to index
- Content preview (first 2000 chars)

## ⚡ Performance

- **Deploy time**: 2-5 minutes
- **Page load**: <1 second
- **DB size**: Original SQLite size
- **Limits**: GitHub Pages has 1GB soft limit

## 🚨 Troubleshooting

### "Failed to download artifacts"
- Check `run_id` is correct
- Check artifacts haven't expired (90-day retention)
- Check `source_repo` is correct format (owner/repo)

### "Pages not showing"
- Check GitHub Pages is enabled in Settings
- Wait 1-2 minutes for deployment
- Check Actions tab for deployment status

### "No databases found"
- Check crawler finished successfully
- Check artifacts were uploaded
- Check you're using correct `run_id`

## 🤝 Integration

You can trigger this from the crawler repo using workflow dispatch or add a step to auto-trigger:

```yaml
- name: Trigger Pages Deployment
  run: |
    gh workflow run deploy.yml -R KomarovAI/web-crawler-pages \
      -f source_repo=KomarovAI/web-crawler \
      -f run_id=${{ github.run_id }}
```

## 📄 License

MIT - Use freely!

---

**Made with ❤️ by the web crawler team**
