# Web Crawling Agent Specification

## Project Overview
- **Project Name**: WebCrawl Agent
- **Type**: AI Agent using LangGraph SDK with multi-source web crawling capabilities
- **Core Functionality**: A LangGraph-based AI agent that crawls websites using Firecrawl and Crawl4AI open-source APIs with multiple crawl modes (single page, depth, sitemap, knowledge graph, deep crawl)
- **Target Users**: Developers, researchers, and AI practitioners needing robust web data extraction

## Technology Stack
- **Framework**: LangGraph SDK (state graph workflow)
- **Crawling Providers**: 
  - Firecrawl Open Source API
  - Crawl4AI
- **Language**: Python 3.10+

## Crawl Modes

### 1. Single Page Mode
- Crawls exactly one URL
- Returns clean markdown content
- No recursive crawling
- **Parameters**: `url` (required)

### 2. Depth Mode
- Crawls starting URL and follows links up to specified depth
- BFS (Breadth-First Search) traversal
- **Parameters**: `url`, `depth` (default: 2), `max_pages` (optional limit)

### 3. Sitemap Mode
- Discovers URLs from sitemap.xml
- Crawls all URLs found in sitemap
- **Parameters**: `url` (sitemap URL or base URL)

### 4. Knowledge Graph Mode
- Crawls and extracts structured knowledge
- Identifies entities, relationships
- Returns knowledge graph (JSON)
- **Parameters**: `url`, `depth`

### 5. Deep Crawl Mode
- Recursively crawls ALL links from any crawled content until end nodes
- No depth limit by default
- Comprehensive web crawling
- **Parameters**: `url`, `max_urls` (optional limit to prevent infinite crawls)

## Graph State Structure

```python
class CrawlState(TypedDict):
    url: str                    # Starting URL
    mode: str                 # crawl mode
    crawled_pages: List[Dict]   # List of crawled page data
    visited_urls: List[str]      # URLs already visited
    pending_urls: List[str]      # URLs waiting to crawl
    extracted_links: List[str] # All discovered links
    knowledge_graph: Dict     # Extracted knowledge (for knowledge mode)
    error: Optional[str]     # Error message if any
    status: str             # "running", "completed", "error"
```

## Node Structure

1. **START** - Entry point, validates input
2. **FETCH_SITEMAP** - For sitemap mode, fetches sitemap XML
3. **CRAWL_PAGE** - Uses Firecrawl/Crawl4AI to crawl a page
4. **EXTRACT_LINKS** - Extracts all links from crawled content
5. **DECIDE_NEXT** - Determines next URLs to crawl based on mode
6. **EXTRACT_KNOWLEDGE** - For knowledge graph mode, extracts entities
7. **END** - Completes crawl and returns results

## Crawler Configuration

### Firecrawl Integration
- Uses `firecrawl-py` package
- Supports: scrape, crawl, search endpoints
- Returns markdown, HTML, or structured JSON

### Crawl4AI Integration
- Uses `crawl4ai` package  
- Async WebCrawler class
- Returns clean markdown, JSON, or HTML

## File Structure

```
/workspace/project/
├── crawler_agent/
│   ├── __init__.py
│   ├── graph.py          # LangGraph state graph definition
│   ├── nodes.py        # Node functions
│   ├── state.py        # State definitions
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── firecrawl.py
│   │   └── crawl4ai.py
│   └── config.py       # Configuration
├── examples/
│   └── example_usage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## API Interface

### Agent Usage

```python
from crawler_agent import CrawlAgent

# Initialize agent with LLM
agent = CrawlAgent(
    llm=llm,
    provider="firecrawl"  # or "crawl4ai"
)

# Single page crawl
result = await agent.crawl(
    url="https://example.com",
    mode="single"
)

# Depth crawl
result = await agent.crawl(
    url="https://example.com",
    mode="depth",
    depth=2
)

# Deep crawl
result = await agent.crawl(
    url="https://example.com",
    mode="deep",
    max_urls=100
)
```

## Output Format

```python
{
    "status": "completed",
    "mode": "depth",
    "url": "https://example.com",
    "crawled_pages": [
        {
            "url": "https://example.com",
            "markdown": "# Example...",
            "links": ["https://example.com/page1", ...],
            "metadata": {"title": "...", "description": "..."}
        }
    ],
    "total_pages": 5,
    "knowledge_graph": {...}  # if knowledge mode
}
```

## Acceptance Criteria

1. ✅ Agent can crawl single pages using Firecrawl
2. ✅ Agent can crawl single pages using Crawl4AI
3. ✅ Supports all 5 crawl modes
4. ✅ State graph properly tracks visited/pending URLs
5. ✅ Returns clean markdown content
6. ✅ Handles errors gracefully
7. ✅ Configurable via environment variables
8. ✅ Comprehensive documentation