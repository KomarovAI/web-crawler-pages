# Web Crawler Pages

Deploy crawled websites to GitHub Pages - automated website archival and hosting.

## Setup

1. This repository receives archives from the [web-crawler](https://github.com/KomarovAI/web-crawler) project
2. Automatic deployment to GitHub Pages happens via GitHub Actions
3. Website is hosted at: https://komarovai.github.io/web-crawler-pages/

## Pages Branch

Deployed content is on the `gh-pages` branch. Configure GitHub Pages to use this branch.

## How It Works

1. web-crawler workflow generates archive
2. Artifacts deployed to `web-crawler-pages` repository
3. `gh-pages` branch is updated with extracted files
4. GitHub Pages automatically publishes the content

## GitHub Pages Configuration

Ensure your repository settings have:
- **Source**: Deploy from branch
- **Branch**: `gh-pages`
- **Folder**: `/ (root)`
