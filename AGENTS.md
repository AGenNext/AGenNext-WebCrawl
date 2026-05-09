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

## Commands
```bash
# Trigger build
curl -X POST "https://api.github.com/repos/AGenNext/AGenNext-WebCrawl/actions/workflows/cd.yml/dispatches" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -d '{"ref": "main"}'
```

## Lessons Learned / Mistakes
1. **Stale Docker Image**: After adding new files (version.py), Coolify had cached old image. Always trigger redeploy after new commits.
2. **GitHub Compare URL**: Relative dates like `{1day}` don't work. Use explicit dates like `{2026-05-08}`.
3. **Org-level Secrets**: For org-level variables, use `${{ vars.NAME }}` (not secrets). Only sensitive data goes in secrets.
4. **Always Verify**: Don't assume app works - test with browser/Playwright to check for errors like ModuleNotFoundError.
5. **Git Push Timeout**: Use token in URL (`https://${GITHUB_TOKEN}@github.com/...`) instead of interactive prompt.
6. **Check Action Logs**: Don't assume what failed - check GitHub action job logs to see exact error.
7. **Wrong API Key**: GitHub token doesn't work for Coolify API - need separate token.
8. **Early Confirmation**: Say "working fine" without Playwright test - caused delay in finding real error.
9. **Playwright API**: `page.context.new_context` doesn't exist - use console event listeners instead.
10. **Confirm Before Save**: Ask user before adding to AGENTS.md - may not want all content saved.
11. **False Positives**: curl returning HTML is NOT success - check actual content for errors.
12. **Docker Typo**: Image name "openautonymyx" vs correct "openautonomyx" - always verify spelling.
13. **Trust but Verify**: Even if code is on GitHub doesn't mean it's deployed - verify actual app.
14. **Workflow Failure**: Don't re-trigger without checking why it failed - check logs first.
15. **No Auto-Deploy**: Adding files locally doesn't auto-deploy - must push to trigger.