# Changelog

All notable changes to Web Crawler Service will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-09

### Added
- Web Crawler Service multi-page Streamlit app
- Landing page with provider info
- Chat page for conversational crawling
- Crawler dashboard with form inputs
- Billing dashboard with credits/plans
- Account settings with API keys
- Login page
- Crawl modes: Single, Depth, Deep/Knowledge, Sitemap
- Provider support: Crawl4AI, Firecrawl
- Depth and max pages/URLs limits
- Test suite with Playwright (48 tests)
- CI/CD pipeline for testing
- Docker Compose deployment

### Fixed
- st.run() error in app.py
- Removed broken Traefik labels
- Updated Docker Compose version to 3.9

### Security
- XSS protection tests
- SQL injection protection tests

### Version
- Semantic versioning implemented
- Version module created (version.py)