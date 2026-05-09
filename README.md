# Web Crawling Agent

A powerful AI-driven web crawling agent built with LangGraph SDK that leverages open-source web crawlers (Firecrawl and Crawl4AI) to extract web content in multiple modes.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Multi-Mode Crawling**: 5 different crawl modes to suit your needs
- **Open Source**: Built on Firecrawl and Crawl4AI open-source APIs
- **LangGraph Powered**: State graph workflow for robust crawling
- **Knowledge Extraction**: Extract structured knowledge from web content
- **Deep Crawling**: Recursively crawl all links until end nodes

## Installation

```bash
pip install -e .
```

Or with specific dependencies:

```bash
pip install crawl4ai firecrawl-py langgraph langchain-core
```

## Quick Start

```python
import asyncio
from crawler_agent import quick_crawl

# Single page crawl
result = asyncio.run(quick_crawl(
    url="https://example.com",
    mode="single"
))

print(result["crawled_pages"][0]["markdown"])
```

## Crawl Modes

### 1. Single Page Mode

Crawls exactly one URL - no recursive crawling.

```python
result = await agent.crawl(url="https://example.com", mode="single")
```

### 2. Depth Mode

Crawls starting URL and follows links up to specified depth.

```python
result = await agent.crawl(
    url="https://example.com",
    mode="depth",
    depth=2,  # Follow links up to 2 levels
    max_pages=10
)
```

### 3. Sitemap Mode

Discovers URLs from sitemap.xml and crawls all found URLs.

```python
result = await agent.crawl(
    url="https://example.com/sitemap.xml",
    mode="sitemap"
)
```

### 4. Knowledge Graph Mode

Crawls and extracts structured knowledge graph (entities and relationships).

```python
result = await agent.crawl(
    url="https://example.com",
    mode="knowledge",
    depth=2
)

# Access knowledge graph
entities = result["knowledge_graph"]["entities"]
relationships = result["knowledge_graph"]["relationships"]
```

### 5. Deep Crawl Mode

Recursively crawls ALL links from any crawled content until end nodes. No depth limit by default.

```python
result = await agent.crawl(
    url="https://example.com",
    mode="deep",
    max_urls=100  # Limit to prevent infinite crawling
)
```

## Configuration

### Environment Variables

```bash
# Optional: Firecrawl API key (for cloud API)
export FIRECRAWL_API_KEY="fc-..."

# Optional: Custom Firecrawl base URL
export FIRECRAWL_BASE_URL="https://api.firecrawl.dev"
```

### Provider Selection

```python
from crawler_agent import CrawlAgent

# Use Crawl4AI (default, open-source)
agent = CrawlAgent(provider="crawl4ai")

# Use Firecrawl
agent = CrawlAgent(provider="firecrawl")
```

## Advanced Usage

### With LangGraph State Graph

```python
from crawler_agent.graph import create_crawl_graph, get_initial_state

# Create the graph
graph = create_crawl_graph()
compiled = graph.compile()

# Create initial state
state = get_initial_state(
    url="https://example.com",
    mode="depth",
    depth=2,
    provider="crawl4ai"
)

# Run the graph
async for result in compiled.astream(state):
    print(result)
```

### With Custom LLM

```python
import os
from openhands.sdk import LLM
from crawler_agent import CrawlAgent

llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=os.getenv("LLM_API_KEY")
)

agent = CrawlAgent(llm=llm, provider="crawl4ai")
result = await agent.crawl(url="https://example.com", mode="single")
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
            "markdown": "# Example Domain\n\nThis domain...",
            "html": "<html>...</html>",
            "links": [
                "https://example.com/page1",
                "https://example.com/page2"
            ],
            "metadata": {
                "title": "Example Domain",
                "description": "Example domain for testing"
            }
        }
    ],
    "total_pages": 5,
    "knowledge_graph": {
        "entities": [...],
        "relationships": [...]
    },
    "error": None
}
```

## Directory Structure

```
crawler_agent/
├── __init__.py          # Package exports
├── agent.py             # CrawlAgent class
├── config.py            # Configuration
├── graph.py             # LangGraph state graph
├── nodes.py             # Graph nodes
├── state.py             # State definitions
└── crawlers/
    ├── __init__.py
    ├── firecrawl.py     # Firecrawl crawler
    └── crawl4ai.py     # Crawl4AI crawler
```

## Requirements

- Python 3.10+
- langgraph >= 0.2.0
- langchain-core >= 0.3.0
- crawl4ai >= 0.3.0
- firecrawl-py >= 1.0.0
- beautifulsoup4 >= 4.12.0
- lxml >= 5.0.0

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Firecrawl](https://firecrawl.dev) - Open source web scraping
- [Crawl4AI](https://crawl4ai.com) - LLM-friendly web crawler
- [LangGraph](https://langchain.dev/langgraph) - State graph workflow# trigger rebuild
