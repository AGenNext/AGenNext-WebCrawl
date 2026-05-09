"""All Tools for LangGraph Agent - Crawlers, OCR, RAG, etc.
Includes LlamaIndex integrations: https://github.com/run-llama/llama_index/
pip install llama-index
"""
from typing import Dict, Any, Callable, List
import asyncio

# Import all integrations
from crawler_agent.crawlers.firecrawl import FirecrawlCrawler
from crawler_agent.crawlers.crawl4ai import Crawl4AICrawler
from crawler_agent.tools import (
    SEOTools, ContentTools, LinkTools, ExportTools, FilterTools,
    ScreenshotTools, FormTools, OCRTools
)
from crawler_agent.skills import AGENT_SKILLS


# ============== LLAMAINDEX INTEGRATIONS ==============

# Try imports from llama-index integrations
try:
    from llama_index.readers import JSONReader, PDFReader, DocxReader
    LLAMA_READERS = True
except ImportError:
    LLAMA_READERS = False

try:
    from llama_index.vector_stores import PineconeVectorStore, WeaviateVectorStore
    LLAMA_VECTOR_STORES = True
except ImportError:
    LLAMA_VECTOR_STORES = False

try:
    from llama_index.embeddings import OpenAIEmbedding, HuggingFaceEmbedding, OllamaEmbedding
    LLAMA_EMBEDDINGS = True
except ImportError:
    LLAMA_EMBEDDINGS = False

try:
    from llama_index.llms import OpenAI, Ollama, Anthropic
    LLAMA_LLMS = True
except ImportError:
    LLAMA_LLMS = False


# ============== RAG WITH LLAMAINDEX ==============

from crawler_agent.rag import RAGFlow, LocalRAGFlow


# ============== CRAWLER TOOLS ==============

async def crawl_firecrawl(url: str, options: Dict = None) -> Dict[str, Any]:
    """Crawl using Firecrawl (open source)"""
    crawler = FirecrawlCrawler()
    try:
        result = await crawler.crawl(url, options or {})
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def crawl_crawl4ai(url: str, options: Dict = None) -> Dict[str, Any]:
    """Crawl using Crawl4AI"""
    crawler = Crawl4AICrawler()
    try:
        result = await crawler.crawl(url, options or {})
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


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
    # Crawlers
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