# AGenNext-WebCrawl Agent

## Project Overview
- Streamlit web crawling app using Firecrawl/Crawl4AI APIs
- Deployed to: http://51.75.251.56:8501
- Repository: AGenNext/AGenNext-WebCrawl
- Docker Image: `openautonomyx/webcrawl-agnxxt:latest`

## GitHub Actions Secrets (Org-Level)
When fixing Docker login failures:
- Use `${{ vars.DOCKERHUB_USERNAME }}` for username (variable)
- Use `${{ secrets.DOCKERHUB_TOKEN }}` for password (secret)
- Set at org level: https://github.com/organizations/AGenNext/settings/

## CI/CD Workflows
- `cd.yml` - Build & Deploy on push to main
- `test.yml` - Run tests on PR/push
- Coolify: `https://vps.openautonomyx.com/api/v1/deploy?uuid=hx8o7igiqdhzumxnykgcycl0`

## Key Files
- `examples/app.py` - Main Streamlit app
- `components/seo_meta.py` - SEO meta tags
- `components/social_share.py` - Social sharing
- `docs/SECRETS_SETUP.md` - Secrets documentation

## Project Commands
```bash
# Build & Run locally
streamlit run examples/app.py

# Run tests
pytest tests/

# Trigger CI/CD deployment
curl -X POST "https://api.github.com/repos/AGenNext/AGenNext-WebCrawl/actions/workflows/cd.yml/dispatches" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -d '{"ref": "main"}'
```

## Agent Guidelines
- Always verify app works after changes - use Playwright or visit the URL
- After adding new files, trigger redeploy before confirming "it works"
- Check GitHub action logs when builds fail - don't assume
- For Docker Hub login in actions: username goes in vars, token in secrets
- Use explicit dates in GitHub compare URLs, not relative