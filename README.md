# Autonomous Researcher

A Jekyll-based GitHub Pages site for autonomous research and discovery.

## Live Site

🌐 https://menuvis1-blip.github.io/autonomous-researcher

## Local Development

### Prerequisites

- Ruby 2.5+ 
- Bundler

### Setup

```bash
bundle install
```

### Run locally

```bash
bundle exec jekyll serve
```

Site will be available at `http://localhost:4000`

## GitHub Pages Configuration

This site is configured to work with GitHub Pages using the `minima` theme.

### Enable GitHub Pages

1. Go to **Settings → Pages** in your repo
2. Set **Source** to "Deploy from a branch"
3. Select branch: `main` / `master`
4. Click **Save**

### Theme

Uses [Minima](https://github.com/jekyll/minima) — a clean, responsive Jekyll theme.

## Project Structure

```
.
├── _config.yml          # Site configuration
├── _layouts/            # Page layouts
├── _includes/           # Reusable components  
├── _posts/              # Blog posts (YYYY-MM-DD-title.md)
├── assets/              # Stylesheets and assets
├── index.md             # Homepage
└── about.md             # About page
```

## Adding Posts

Create new posts in `_posts/` with naming convention:
```
YYYY-MM-DD-title-of-post.md
```

Front matter:
```yaml
---
layout: post
title: "Your Post Title"
date: 2025-02-20 12:00:00 +0000
categories: category1 category2
---
```

## Customization

Edit `_config.yml` to change:
- Site title and description
- Author name and email
- Social links
- Theme settings
