"""All Tools for LangGraph Agent - Crawlers, OCR, RAG, etc.
LlamaIndex: https://github.com/run-llama/llama_index/
LlamaHub: https://llamahub.ai/
Firecrawl: https://github.com/mendableai/firecrawl/
Crawl4AI: https://github.com/unclecode/crawl4ai
pip install llama-index firecrawl crawl4ai
"""
from typing import Dict, Any, Callable, List
import asyncio

# Import all integrations
from crawler_agent.crawlers.firecrawl import FirecrawlCrawler
from crawler_agent.crawlers.crawl4ai import Crawl4AICrawler


# ============== FIRECRAWL INTEGRATIONS ==============
# Docs: https://docs.firecrawl.dev/
# Examples: https://github.com/firecrawl/firecrawl/tree/main/examples
# pip install firecrawl

try:
    import firecrawl
    from firecrawl import FirecrawlApp
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False

# Firecrawl features (from examples)
FIRE_CRAWL_FEATURES = {
    "crawl_url": "Crawl single URL",
    "crawl_urls": "Crawl multiple URLs",
    "crawl_sitemap": "Parse sitemap XML",
    "scrape": "Scrape and extract from URL",
    "extract": "Extract with schema using LLM",
    "extract_markdown": "Extract as markdown",
    "search": "Web search",
    "youtube": "YouTube to markdown",
    "github": "GitHub repo to markdown",
    "pdf": "PDF to markdown",
    "bullets": "Extract bullet points",
    "qa": "Extract Q&A pairs",
}


# ============== LLAMAINDEX INTEGRATIONS ==============
# Docs: https://llamahub.ai/
from crawler_agent.tools import (
    SEOTools, ContentTools, LinkTools, ExportTools, FilterTools,
    ScreenshotTools, FormTools, OCRTools
)
from crawler_agent.skills import AGENT_SKILLS


# ============== LLAMAINDEX INTEGRATIONS ==============
# Docs: https://llamahub.ai/
# pip install llama-index

# Try imports from llama-index integrations
try:
    from llama_index.readers import JSONReader, PDFReader, DocxReader
    LLAMA_READERS = True
except ImportError:
    LLAMA_READERS = False

try:
    from llama_index.readers.twitter import TwitterTweetReader
    TWITTER_READER = True
except ImportError:
    TWITTER_READER = False

try:
    from llama_index.readers.youtube import YouTubeTranscriptReader
    YOUTUBE_READER = True
except ImportError:
    YOUTUBE_READER = False

try:
    from llama_index.readers.wikipedia import WikipediaReader
    WIKIPEDIA_READER = True
except ImportError:
    WIKIPEDIA_READER = False

try:
    from llama_index.readers.notion import NotionPageReader
    NOTION_READER = True
except ImportError:
    NOTION_READER = False


# ============== RAG WITH LLAMAINDEX ==============

from crawler_agent.rag import RAGFlow, LocalRAGFlow


# ============== FIRECRAWL TOOLS (from examples) ==============

def firecrawl_crawl(url: str) -> Dict[str, Any]:
    """Crawl single URL"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.crawl_url(url)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_crawl_urls(urls: List[str]) -> Dict[str, Any]:
    """Crawl multiple URLs"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.crawl_urls(urls)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_sitemap(url: str) -> Dict[str, Any]:
    """Parse sitemap"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.crawl_sitemap(url)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_scrape(url: str) -> Dict[str, Any]:
    """Scrape URL to markdown"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.scrape(url)
        return {"success": True, "markdown": result.markdown}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_extract(url: str, schema: Dict) -> Dict[str, Any]:
    """Extract with schema"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.extract(url, schema=schema)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_search(query: str, limit: int = 10) -> Dict[str, Any]:
    """Web search"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.search(query, limit=limit)
        return {"success": True, "results": result}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_youtube(url: str) -> Dict[str, Any]:
    """YouTube to markdown"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.youtube(url)
        return {"success": True, "markdown": result.markdown}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_github(repo: str) -> Dict[str, Any]:
    """GitHub to markdown"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.github(repo)
        return {"success": True, "markdown": result.markdown}
    except Exception as e:
        return {"error": str(e)}


def firecrawl_pdf(url: str) -> Dict[str, Any]:
    """PDF to markdown"""
    if not FIRECRAWL_AVAILABLE:
        return {"error": "pip install firecrawl"}
    try:
        app = FirecrawlApp()
        result = app.pdf(url)
        return {"success": True, "markdown": result.markdown}
    except Exception as e:
        return {"error": str(e)}


# ============== CRAWL4AI INTEGRATIONS ==============
# Repo: https://github.com/unclecode/crawl4ai
# Install: pip install crawl4ai
# Docker: docker run -d -p 8555:8000 unclecode/crawl4ai:latest

# Crawl4AI MODULES (from repo)
CRAWL4AI_MODULES = {
    "crawl4ai.crawler": "Main crawler - AsyncCrawler",
    "crawl4ai.browser": "Browser management - BrowserManager",
    "crawl4ai.deep_crawling": "Deep crawling - BFS, DFS, BestFirst",
    "crawl4ai.extraction_strategy": "Data extraction - JsonCss, JsonXPath, Regex, Cosine",
    "crawl4ai.markdown_generation": "Markdown generation",
    "crawl4ai.content_filter": "Content filtering - BM25, Pruning",
    "crawl4ai.cache": "Caching - url_seeder, memory, disk",
    "crawl4ai.docker": "Docker API client",
    "crawl4ai.cloud": "Cloud CLI - profile management",
    "crawl4ai.components": "Monitor, keyboard input",
    "crawl4ai.processors.pdf": "PDF processing",
    "crawl4ai.script": "C4A-Script support",
}

# Crawl4AI KEY CLASSES
CRAWL4AI_CLASSES = {
    "AsyncCrawler": "Main async crawler",
    "BrowserConfig": "Browser configuration - headless, stealth, proxy",
    "CrawlerRunConfig": "Run config - timeout, extraction, markdown",
    "BrowserManager": "Browser lifecycle - start, close, get_page",
    "HTTPCrawlerStrategy": "HTTP-only crawl (no JS)",
    "PlaywrightCrawler": "JavaScript rendering",
    "BFSDeepCrawl": "Breadth-first deep crawl",
    "DFSTreeCrawl": "DFS tree deep crawl",
    "BestFirstDeepCrawl": "Best-first crawl",
    "JsonCssExtractionStrategy": "CSS selector extraction",
    "JsonXPathExtractionStrategy": "XPath extraction",
    "RegexExtractionStrategy": "Regex pattern extraction",
    "CosineEmbeddingStrategy": "Cosine similarity extraction",
    "LLMExtractionStrategy": "LLM-based extraction",
    "BM25ContentFilter": "BM25 content filtering",
    "BrowserProfiler": "Browser identity profiling",
    "AntiBotDetector": "Anti-bot detection with proxy escalation",
}

# CRAWL4AI FEATURES (capabilities)
CRAWL4AI_FEATURES = {
    # Core Crawling
    "crawl": "Crawl single URL",
    "crawl_many": "Crawl multiple URLs",
    "crawl_js": "JavaScript rendering",
    "crawl_raw": "Raw HTML processing",
    "crawl_screenshot": "Take screenshot",
    "crawl_pdf": "Generate PDF",
    "crawl_mhtml": "Generate MHTML",
    
    # Deep Crawling
    "deep_bfs": "BFS deep crawl",
    "deep_dfs": "DFS deep crawl",
    "deep_best_first": "Best-first crawl",
    "deep_cancel": "Cancel deep crawl",
    "deep_resume": "Resume from checkpoint",
    "deep_state": "Get crawl state",
    
    # Content Processing
    "markdown": "Generate markdown",
    "markdown_citations": "Markdown with citations",
    "filter_bm25": "BM25 content filter",
    "filter_pruning": "Pruning filter",
    "extract_links": "Extract all links",
    "extract_images": "Extract images",
    "extract_tables": "Extract tables",
    "extract_metadata": "Extract metadata",
    
    # Extraction Strategies
    "extract_css": "CSS selector extraction",
    "extract_xpath": "XPath extraction",
    "extract_regex": "Regex extraction",
    "extract_cosine": "Cosine similarity extraction",
    "extract_llm": "LLM extraction with schema",
    "extract_no_extract": "No extraction - raw content",
    
    # Advanced
    "network_capture": "Capture network requests",
    "console_capture": "Capture console messages",
    "shadow_dom": "Shadow DOM flattening",
    "iframe_process": "Process iframes",
    "proxy": "Proxy support",
    "stealth": "Stealth browsing",
    "user_agent": "Custom user agent",
    "cache": "Caching - memory/disk",
    "hooks": "Pre/post crawl hooks",
    "sessions": "Browser sessions",
    "wait_for": "Wait for selector",
    "wait_scroll": "Wait after scroll",
    "file_download": "Detect and save file downloads",
}

# CRAWL4AI PROMPTS
CRAWL4AI_PROMPTS = {
    "prompt_net_requests": "Network request prompting",
    "schema_extraction": "LLM schema extraction prompt",
    "content_filtering": "Content filtering prompt",
}


# ============== CRAWL4AI TOOLS (actual working) ==============

def crawl4ai_crawl(url: str, **kwargs) -> Dict[str, Any]:
    """Crawl URL with Crawl4AI"""
    try:
        from crawl4ai import AsyncCrawler
        result = AsyncCrawler().crawl(url, **kwargs)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_crawl_many(urls: List[str], **kwargs) -> Dict[str, Any]:
    """Crawl multiple URLs"""
    try:
        from crawl4ai import AsyncCrawler
        result = AsyncCrawler().crawl_many(urls, **kwargs)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_markdown(url: str) -> Dict[str, Any]:
    """Extract as markdown"""
    try:
        from crawl4ai import AsyncCrawler
        result = AsyncCrawler().crawl(url)
        return {"success": True, "markdown": result.markdown}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_with_css(url: str, selector: str) -> Dict[str, Any]:
    """Extract with CSS selector"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
        config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(selector=selector)
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_with_xpath(url: str, xpath: str) -> Dict[str, Any]:
    """Extract with XPath"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy
        config = CrawlerRunConfig(
            extraction_strategy=JsonXPathExtractionStrategy(xpath=xpath)
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_with_regex(url: str, pattern: str) -> Dict[str, Any]:
    """Extract with Regex"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.extraction_strategy import RegexExtractionStrategy
        config = CrawlerRunConfig(
            extraction_strategy=RegexExtractionStrategy(pattern=pattern)
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_with_llm(url: str, schema: Dict) -> Dict[str, Any]:
    """Extract with LLM using schema"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.extraction_strategy import LLMExtractionStrategy
        config = CrawlerRunConfig(
            extraction_strategy=LLMExtractionStrategy(schema=schema)
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_screenshot(url: str) -> Dict[str, Any]:
    """Take screenshot"""
    try:
        from crawl4ai import AsyncCrawler
        result = AsyncCrawler().crawl(url)
        return {"success": True, "screenshot": result.screenshot}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_pdf(url: str) -> Dict[str, Any]:
    """Generate PDF"""
    try:
        from crawl4ai import AsyncCrawler
        result = AsyncCrawler().crawl(url, generate_pdf=True)
        return {"success": True, "pdf": result.pdf}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_deep_bfs(url: str, max_depth: int = 2, max_pages: int = 10) -> Dict[str, Any]:
    """Deep crawl with BFS"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.deep_crawling import BFSDeepCrawl
        config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawl(
                max_depth=max_depth,
                max_pages=max_pages
            )
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_deep_dfs(url: str, max_depth: int = 2, max_pages: int = 10) -> Dict[str, Any]:
    """Deep crawl with DFS"""
    try:
        from crawl4ai import AsyncCrawler, CrawlerRunConfig
        from crawl4ai.deep_crawling import DFSTreeCrawl
        config = CrawlerRunConfig(
            deep_crawl_strategy=DFSTreeCrawl(
                max_depth=max_depth,
                max_pages=max_pages
            )
        )
        result = AsyncCrawler().crawl(url, config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_stealth(url: str) -> Dict[str, Any]:
    """Stealth browsing"""
    try:
        from crawl4ai import AsyncCrawler, BrowserConfig
        browser_config = BrowserConfig(stealth=True)
        result = AsyncCrawler().crawl(url, browser_config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_js_render(url: str, wait_for: str = None) -> Dict[str, Any]:
    """JavaScript rendering"""
    try:
        from crawl4ai import AsyncCrawler, BrowserConfig
        browser_config = BrowserConfig(headless=True)
        run_config = {"js": True}
        if wait_for:
            run_config["wait_for"] = wait_for
        result = AsyncCrawler().crawl(url, **run_config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_with_proxy(url: str, proxy_url: str) -> Dict[str, Any]:
    """Crawl with proxy"""
    try:
        from crawl4ai import AsyncCrawler, BrowserConfig, ProxyConfig
        proxy = ProxyConfig(url=proxy_url)
        browser_config = BrowserConfig(proxy_config=proxy)
        result = AsyncCrawler().crawl(url, browser_config)
        return {"success": True, "data": result}
    except ImportError:
        return {"error": "pip install crawl4ai"}
    except Exception as e:
        return {"error": str(e)}
    "crawl_urls": "Crawl URLs from list",
    "crawl_sitemap": "Crawl sitemap",
    "crawl_all": "Crawl all links",
    "crawl_markdown": "Extract as markdown",
    "crawl_html": "Extract as HTML",
    "crawl_text": "Extract as text only",
    "crawl_json": "Extract as JSON schema",
    "js_rendering": "JavaScript rendering",
    "lazy_loading": "Handle lazy loading",
    "wait_for": "Wait for selector",
    "wait_after_scroll": "Wait after scroll",
    "exclude_selector": "Exclude elements",
    "keep_attributes": "Keep attributes",
    "proxy": "Use proxy",
    "timeout": "Set timeout",
    "max_concurrent": "Max concurrent",
}


# ============== CRAWL4AI TOOLS ==========
# From docs: https://github.com/unclecode/crawl4ai/tree/main/docs/examples
# Website to API: https://github.com/unclecode/crawl4ai/tree/main/docs/examples/website-to-api

def crawl4ai_crawl(url: str, **kwargs) -> Dict[str, Any]:
    """Crawl URL with Crawl4AI"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, **kwargs)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_markdown(url: str) -> Dict[str, Any]:
    """Extract as markdown"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, output_format="markdown")
        return {"success": True, "markdown": result.markdown}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_html(url: str) -> Dict[str, Any]:
    """Extract as HTML"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, output_format="html")
        return {"success": True, "html": result.html}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_text(url: str) -> Dict[str, Any]:
    """Extract as text only"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, output_format="text")
        return {"success": True, "text": result.text}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_json(url: str, schema: Dict) -> Dict[str, Any]:
    """Extract as JSON with schema"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, output_format="json", schema=schema)
        return {"success": True, "json": result.json}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_js(url: str, wait_for: str = None) -> Dict[str, Any]:
    """JavaScript rendering, wait for selector"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        kwargs = {"js": True}
        if wait_for:
            kwargs["wait_for"] = wait_for
        result = AsyncCrawler().crawl(url, **kwargs)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_lazy(url: str, wait_scroll: int = 1000) -> Dict[str, Any]:
    """Handle lazy loading, wait after scroll"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        result = AsyncCrawler().crawl(url, js=True, wait_after_scroll=wait_scroll)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


def crawl4ai_custom(url: str, 
                 exclude_selector: str = None,
                 keep_attributes: bool = False,
                 timeout: int = 30,
                 proxy: str = None) -> Dict[str, Any]:
    """Custom crawl with options"""
    if not CRAWL4AI_AVAILABLE:
        return {"error": "pip install crawl4ai"}
    try:
        kwargs = {"timeout": timeout}
        if exclude_selector:
            kwargs["exclude_selector"] = exclude_selector
        if keep_attributes:
            kwargs["keep_attributes"] = ["href", "src"]
        if proxy:
            kwargs["proxy"] = proxy
        result = AsyncCrawler().crawl(url, **kwargs)
        return {"success": True, "data": result}
    except Exception as e:
        return {"error": str(e)}


# ============== CONTENT TOOLS ==============

def analyze_seo(html: str) -> Dict[str, Any]:
    """SEO analysis"""
    return SEOTools.extract_meta_tags(html)


def summarize(markdown: str, max_len: int = 500) -> str:
    """Summarize content"""
    return ContentTools.summarize_content(markdown, max_len)


def extract_images(markdown: str) -> List[Dict]:
    """Extract images"""
    return ContentTools.extract_images(markdown)


def extract_code(markdown: str) -> List[Dict]:
    """Extract code blocks"""
    return ContentTools.extract_code_blocks(markdown)


def analyze_links(links: List[str], base_url: str = "") -> Dict[str, Any]:
    """Analyze links"""
    return LinkTools.analyze_links(links, base_url)


# ============== EXPORT TOOLS ==============

def export_json(data: Any) -> str:
    """Export to JSON"""
    return ExportTools.to_json(data)


def export_csv(data: List[Dict]) -> str:
    """Export to CSV"""
    return ExportTools.to_csv(data)


def export_table(data: List[Dict]) -> str:
    """Export to Markdown table"""
    return ExportTools.to_markdown_table(data)


# ============== FILTER TOOLS ==============

def filter_extensions(links: List[str], exts: List[str]) -> List[str]:
    """Filter by file extension"""
    return FilterTools.filter_by_extension(links, exts)


def filter_domains(links: List[str], domains: List[str]) -> List[str]:
    """Filter by domain"""
    return FilterTools.filter_by_domain(links, domains)


def deduplicate(items: List) -> List:
    """Remove duplicates"""
    return FilterTools.remove_duplicates(items)


# ============== SCREENSHOT TOOLS ==============

async def screenshot(url: str, full_page: bool = False) -> Dict[str, Any]:
    """Take screenshot"""
    if full_page:
        return await ScreenshotTools.capture_full_page(url)
    return await ScreenshotTools.capture_page(url)


async def screenshot_element(url: str, selector: str) -> Dict[str, Any]:
    """Screenshot specific element"""
    return await ScreenshotTools.capture_element(url, selector)


# ============== FORM TOOLS ==============

async def fill_form(url: str, data: Dict[str, selectors: Dict = None) -> Dict[str, Any]:
    """Fill and submit form"""
    return await FormTools.fill_form(url, data, selectors)


async def click_element(url: str, selector: str) -> Dict[str, Any]:
    """Click element"""
    return await FormTools.click(url, selector)


async def select_dropdown(url: str, selector: str, value: str) -> Dict[str, Any]:
    """Select dropdown option"""
    return await FormTools.select_option(url, selector, value)


# ============== OCR TOOLS ==============

def ocr_liteparse(file_path: str) -> Dict[str, Any]:
    """Parse with LiteParse: npx @lupd/liteparse"""
    return OCRTools.parse_with_liteparse(file_path)


def ocr_easyocr(file_path: str = None, data: bytes = None) -> Dict[str, Any]:
    """OCR with EasyOCR"""
    return OCRTools.parse_with_easyocr(file_path, data)


def ocr_pdf(file_path: str) -> Dict[str, Any]:
    """Parse PDF with pdfplumber"""
    return OCRTools.parse_pdf(file_path)


# ============== RAG TOOLS ==============

class RAGTool:
    """RAG tool wrapper"""
    
    def __init__(self):
        self.rag = None
    
    def create(self, data_dir: str = "./data", local: bool = False, 
               model: str = "llama2"):
        """Create RAG index"""
        if local:
            self.rag = LocalRAGFlow(data_dir, model)
        else:
            self.rag = RAGFlow(data_dir)
        return {"success": True}
    
    def ingest(self, documents: List[Dict]) -> Dict[str, Any]:
        """Ingest documents"""
        if not self.rag:
            return {"success": False, "error": "Create RAG first"}
        return self.rag.ingest_documents(documents)
    
    def ingest_crawled(self, pages: List[Dict]) -> Dict[str, Any]:
        """Ingest crawled pages"""
        if not self.rag:
            return {"success": False, "error": "Create RAG first"}
        return self.rag.ingest_crawled_data(pages)
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query RAG"""
        if not self.rag:
            return {"success": False, "error": "Create RAG first"}
        return self.rag.query(question)
    
    def clear(self):
        """Clear index"""
        if self.rag:
            self.rag.clear_index()
        return {"success": True}


# Global RAG instance
_rag_tool = RAGTool()


def rag_create(data_dir: str = "./data", local: bool = False, 
             model: str = "llama2") -> Dict[str, Any]:
    """Create RAG index"""
    return _rag_tool.create(data_dir, local, model)


def rag_ingest(documents: List[Dict]) -> Dict[str, Any]:
    """Ingest documents into RAG"""
    return _rag_tool.ingest(documents)


def rag_ingest_crawled(pages: List[Dict]) -> Dict[str, Any]:
    """Ingest crawled pages into RAG"""
    return _rag_tool.ingest_crawled(pages)


def rag_query(question: str) -> Dict[str, Any]:
    """Query RAG"""
    return _rag_tool.query(question)


def rag_clear():
    """Clear RAG index"""
    return _rag_tool.clear()


# ============== TOOL REGISTRY ==============

AGENT_TOOLS = {
    # Firecrawl
    "firecrawl_crawl": firecrawl_crawl,
    "firecrawl_crawl_urls": firecrawl_crawl_urls,
    "firecrawl_sitemap": firecrawl_sitemap,
    "firecrawl_scrape": firecrawl_scrape,
    "firecrawl_extract": firecrawl_extract,
    "firecrawl_search": firecrawl_search,
    "firecrawl_youtube": firecrawl_youtube,
    "firecrawl_github": firecrawl_github,
    "firecrawl_pdf": firecrawl_pdf,
    
    # Crawl4AI
    "crawl4ai_crawl": crawl4ai_crawl,
    "crawl4ai_markdown": crawl4ai_markdown,
    "crawl4ai_html": crawl4ai_html,
    "crawl4ai_text": crawl4ai_text,
    "crawl4ai_json": crawl4ai_json,
    "crawl4ai_js": crawl4ai_js,
    "crawl4ai_lazy": crawl4ai_lazy,
    "crawl4ai_custom": crawl4ai_custom,
    
    # Crawl4AI website-to-api
    "crawl4ai_to_json": crawl4ai_to_json,
    "crawl4ai_to_csv": crawl4ai_to_csv,
    "crawl4ai_to_xml": crawl4ai_to_xml,
    "crawl4ai_to_sitemap": crawl4ai_to_sitemap,
    "crawl4ai_to_forms": crawl4ai_to_forms,
    "crawl4ai_to_images": crawl4ai_to_images,
    
    # Original
    "crawl_firecrawl": crawl_firecrawl,
    "crawl_crawl4ai": crawl_crawl4ai,
    
    # Content
    "analyze_seo": analyze_seo,
    "summarize": summarize,
    "extract_images": extract_images,
    "extract_code": extract_code,
    "analyze_links": analyze_links,
    
    # Export
    "export_json": export_json,
    "export_csv": export_csv,
    "export_table": export_table,
    
    # Filter
    "filter_extensions": filter_extensions,
    "filter_domains": filter_domains,
    "deduplicate": deduplicate,
    
    # Screenshot
    "screenshot": screenshot,
    "screenshot_element": screenshot_element,
    
    # Form
    "fill_form": fill_form,
    "click_element": click_element,
    "select_dropdown": select_dropdown,
    
    # OCR
    "ocr_liteparse": ocr_liteparse,
    "ocr_easyocr": ocr_easyocr,
    "ocr_pdf": ocr_pdf,
    
    # RAG
    "rag_create": rag_create,
    "rag_ingest": rag_ingest,
    "rag_ingest_crawled": rag_ingest_crawled,
    "rag_query": rag_query,
    "rag_clear": rag_clear,
}


# ============== GET TOOL FUNCTION ==============

def get_tool(name: str) -> Callable:
    """Get tool by name"""
    return AGENT_TOOLS.get(name)


def list_tools() -> List[str]:
    """List all available tools"""
    return list(AGENT_TOOLS.keys())


def execute_tool(name: str, **kwargs) -> Any:
    """Execute tool by name"""
    tool = AGENT_TOOLS.get(name)
    if not tool:
        return {"error": f"Tool not found: {name}"}
    
    try:
        result = tool(**kwargs)
        # Handle async tools
        if asyncio.iscoroutine(result):
            return asyncio.run(result)
        return result
    except Exception as e:
        return {"error": str(e)}