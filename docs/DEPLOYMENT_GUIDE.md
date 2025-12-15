# 🚀 Deployment Guide - web-crawler-pages

## Overview

This guide explains how to deploy crawled websites to GitHub Pages using the new production-ready workflows.

## Quick Start

### 1. Prepare Your Crawled Website

First, run the crawler to get your artifact:

```bash
# From web-crawler repo
git clone https://github.com/KomarovAI/web-crawler
cd web-crawler
# Configure and run crawler...
```

Note the **Run ID** from your crawler run (visible in GitHub Actions).

### 2. Verify Artifact Quality

Before deploying, verify your artifact is valid:

```
1. Go to: https://github.com/KomarovAI/web-crawler-pages/actions
2. Click: "🔍 Verify & Validate Artifacts"
3. Click: "Run workflow"
4. Fill in:
   - source_repo: KomarovAI/web-crawler
   - run_id: <your-run-id>
   - site_domain: callmedley-com
5. Click: "Run workflow"
```

**Expected output:**
```
✅ PASSED: All databases verified successfully!
Total pages: 379
Total size: 131.80 MB
```

### 3. Deploy to GitHub Pages

Once verification passes:

```
1. Go to: https://github.com/KomarovAI/web-crawler-pages/actions
2. Click: "🚀 Deploy to GitHub Pages"
3. Click: "Run workflow"
4. Fill in same parameters as verification
5. Click: "Run workflow"
6. Wait 3-5 minutes for deployment
7. Visit: https://komarovai.github.io/web-crawler-pages/
```

## Workflows Explained

### 🔍 Verify & Validate Artifacts

**What it does:** Comprehensive validation before deployment

**Checks performed:**
- ✅ SQLite file format validation
- ✅ Database integrity check (PRAGMA integrity_check)
- ✅ Foreign key constraint validation
- ✅ Table structure verification
- ✅ Page count validation
- ✅ Quick database check (PRAGMA quick_check)
- ✅ Record accessibility testing
- ✅ File size sanity checks

**Input parameters:**
| Parameter | Required | Example | Notes |
|-----------|----------|---------|-------|
| source_repo | Yes | KomarovAI/web-crawler | owner/repo format |
| run_id | Yes | 20248768651 | From crawler run |
| site_domain | Yes | callmedley-com | Folder name |

**Output:**
- Detailed verification report
- SHA256 artifact hash
- Page count
- Database integrity status

**When to use:**
- Before every deployment
- After crawler completed
- To validate artifact quality

**Run time:** ~2 minutes

---

### 🚀 Deploy to GitHub Pages

**What it does:** Full deployment pipeline with automatic verification

**Pipeline stages:**

1. **Pre-Deploy Verification** (Optional, default: enabled)
   - Runs the verify workflow
   - Fails if artifacts don't pass validation
   - Can be disabled with `auto_verify: false`

2. **Prepare Deployment**
   - Download artifacts from source repo
   - Generate deployment ID
   - Extract artifact size and page count

3. **Build Static Site**
   - Extract data from SQLite database
   - Generate HTML pages for each crawled URL
   - Create index pages with site listings
   - Generate metadata.json for each site

4. **Deploy to Pages**
   - Configure GitHub Pages
   - Build Jekyll site
   - Upload to Pages artifact storage
   - Deploy via GitHub Pages

5. **Verify Deployment**
   - Test Pages URL accessibility
   - Retry if Pages is still building
   - Print deployment summary

**Input parameters:**
| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| source_repo | string | Yes | - | Crawler repo |
| run_id | string | Yes | - | Artifact run ID |
| site_domain | string | Yes | - | Folder name |
| auto_verify | boolean | No | true | Verify before deploy |

**Output files:**
```
sites/
├── DOMAIN/
│   ├── index.html           # Site overview
│   ├── DOMAIN.db            # SQLite database
│   ├── pages/
│   │   ├── page-00001.html
│   │   ├── page-00002.html
│   │   └── ...
│   └── metadata.json        # Site metadata
├── ...
└── .deployment/
    └── info.json            # Deployment info
```

**Generated HTML files:**
- **sites/index.html** - Main archive page with all sites
- **sites/DOMAIN/index.html** - Site overview with all pages
- **sites/DOMAIN/pages/page-NNNNN.html** - Individual page content

**Run time:** 5-10 minutes total

---

### 🚀 Emergency Rollback

**What it does:** Quickly revert to previous deployment if something breaks

**Usage:**

```
1. Go to: https://github.com/KomarovAI/web-crawler-pages/actions
2. Click: "🚀 Emergency Rollback"
3. Click: "Run workflow"
4. Options:
   - Leave empty to rollback to previous deployment
   - Or specify exact commit SHA
5. Click: "Run workflow"
6. Wait 2-3 minutes
```

**Input parameters:**
| Parameter | Type | Required | Notes |
|-----------|------|----------|-------|
| rollback_commit | string | No | Specific commit SHA |
| rollback_to_previous | boolean | No | Auto-detect previous |

**When to use:**
- Deployment broke GitHub Pages
- Need to quickly restore previous version
- Testing new features and need fallback

**Run time:** ~2 minutes

---

## Verification Report Explained

When you run the verification workflow, you'll see output like:

```
============================================================
🔍 DATABASE VERIFICATION REPORT
============================================================

📦 Found 1 database file(s)

Domain: callmedley_com
  File: callmedley_com.db
  Size: 131.80 MB (138207380 bytes)
    ✅ Pages: 379
    ✅ Integrity: OK (PRAGMA check passed)
    ✅ Foreign keys: OK
    ✅ Record accessibility: OK

============================================================
📊 VERIFICATION SUMMARY
============================================================
Total databases: 1
Total pages: 379
Total assets: 0
Total size: 131.80 MB

✅ Valid databases: 1/1
✅ PASSED: All databases verified successfully!
============================================================
```

### Common Issues

**❌ FAIL: No database files found!**
- Check source_repo is correct
- Check run_id is correct
- Verify crawler actually created artifacts
- Check artifact hasn't expired (90-day retention)

**❌ FAIL: Missing 'pages' table**
- Crawler schema incompatible
- Database corrupted
- Wrong artifact downloaded

**❌ FAIL: Database corruption detected**
- Database file is corrupted
- Partial download (incomplete artifact)
- Hardware/storage issue

**⚠️ WARNING: Database is suspiciously small**
- Crawler may not have run successfully
- Website may have very few pages
- Check crawler output logs

---

## Deployment Details

### Generated HTML Structure

#### Main Index (sites/index.html)
```html
<title>🕷️ Crawled Sites Archive</title>
<!-- Grid of cards for each domain -->
<!-- Shows: domain, page count, size, links -->
```

#### Site Index (sites/DOMAIN/index.html)
```html
<title>DOMAIN - Crawled Pages</title>
<!-- Grid of page cards -->
<!-- Shows: title, URL, status code, link to page -->
```

#### Individual Page (sites/DOMAIN/pages/page-NNNNN.html)
```html
<title>Page Title</title>
<!-- Full page metadata -->
<!-- Status code badge -->
<!-- First 5000 chars of content -->
<!-- Navigation back to site/main index -->
```

### Metadata Files

**sites/DOMAIN/metadata.json**
```json
{
  "domain": "callmedley_com",
  "total_pages": 379,
  "crawled_at": "2025-12-15T00:31:46Z",
  "pages": [
    {
      "id": 1,
      "url": "https://callmedley.com",
      "title": "Home",
      "status": 200,
      "file": "pages/page-00001.html"
    },
    ...
  ]
}
```

**.deployment/info.json**
```json
{
  "deployment_id": "20250215-225320-123456789",
  "deployed_at": "2025-12-15T22:53:20Z",
  "deployed_by": "KomarovAI",
  "workflow_run": "123456789",
  "source_repo": "KomarovAI/web-crawler",
  "source_run_id": "20248768651",
  "page_count": "379",
  "artifact_size": "131.80 MB"
}
```

---

## Troubleshooting

### Pages not showing after deployment

```
1. Check deployment status
   Settings → Pages → Check for green checkmark

2. Wait 1-2 minutes
   GitHub Pages needs time to build

3. Check Actions tab
   Look for "pages build and deployment" status

4. Clear browser cache
   Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)

5. Try URL directly
   https://komarovai.github.io/web-crawler-pages/index.html
```

### Verification fails with "Database corruption"

```
1. Re-run crawler
   Artifact may be incomplete

2. Check crawler logs
   See what domains were crawled

3. Download artifact manually
   Verify file size matches

4. Check storage space
   GitHub has 1GB soft limit on Pages
```

### Deployment timeout

```
1. Check artifact size
   May be too large for Pages

2. Split into multiple deployments
   Deploy fewer pages per run

3. Check network
   Download speed may be slow

4. Try again
   Temporary GitHub outage
```

### Site pages not rendering correctly

```
1. Check HTML generation
   Look at raw HTML file

2. Check content encoding
   May have special characters

3. Check database schema
   May have changed in crawler

4. Check page count
   Metadata shows expected pages
```

---

## Security Considerations

### ✅ What's safe
- Public websites (no sensitive data)
- Non-interactive snapshots
- No credentials stored
- OIDC authentication for Pages

### ⚠️ Be careful with
- Websites with personal information
- Password-protected sites
- User data or email addresses
- Large databases (limits)

### 🔒 Best practices
- Only archive public websites
- Review content before deployment
- Set repo to private if concerned
- Regularly clean up old deployments

---

## Performance Tips

### Optimize for GitHub Pages

1. **Limit page count**
   - Pages has 1GB soft limit
   - 1000+ pages = ~500MB typical

2. **Compress database**
   - Run VACUUM in crawler
   - Reduces size 10-30%

3. **Limit content**
   - Crawl fewer pages per run
   - Split large sites into multiple domains

4. **Clean up old deployments**
   - Delete old site folders
   - Reduces repo size

### Monitoring

- Check Pages status regularly
- Monitor artifact download speed
- Watch for deployment failures
- Review generated HTML quality

---

## Advanced Usage

### Programmatic Deployment

```bash
# From CI/CD pipeline
gh workflow run deploy-to-pages.yml \
  -f source_repo=KomarovAI/web-crawler \
  -f run_id=${{ github.run_id }} \
  -f site_domain=mysite-com
```

### Verify without deploying

```bash
# Just run verification
gh workflow run verify-artifact.yml \
  -f source_repo=KomarovAI/web-crawler \
  -f run_id=20248768651 \
  -f site_domain=callmedley-com
```

### Deploy without verification

```bash
# Skip auto-verify for speed
gh workflow run deploy-to-pages.yml \
  -f source_repo=KomarovAI/web-crawler \
  -f run_id=20248768651 \
  -f site_domain=callmedley-com \
  -f auto_verify=false
```

---

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [web-crawler Repository](https://github.com/KomarovAI/web-crawler)

---

## Support

If you encounter issues:

1. Check the workflow logs in GitHub Actions
2. Review this guide's troubleshooting section
3. Check the verification report for details
4. Open an issue on the repository

---

**Last updated:** 2025-12-16
**Workflow version:** 1.0.0
