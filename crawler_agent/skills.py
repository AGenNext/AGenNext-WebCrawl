"""Skills for the Web Crawling Agent"""
from typing import Dict, Any, List
from crawler_agent.tools import SEOTools, ContentTools, LinkTools, ExportTools, FilterTools


class AnalyzeSEOSkill:
    """Analyze SEO aspects of crawled content"""
    
    name = "analyze_seo"
    description = "Analyze SEO meta tags and content structure"
    
    @staticmethod
    def execute(content: str, content_type: str = "html") -> Dict[str, Any]:
        """Execute SEO analysis"""
        if content_type == "html":
            meta_tags = SEOTools.extract_meta_tags(content)
        else:
            meta_tags = {}
        
        if content_type == "markdown":
            headings = SEOTools.extract_headings(content)
            readability = SEOTools.analyze_readability(content)
        else:
            headings = {}
            readability = {}
        
        return {
            "meta_tags": meta_tags,
            "headings": headings,
            "readability": readability,
            "score": "good" if meta_tags.get("description") else "needs_optimization"
        }


class SummarizeSkill:
    """Summarize content"""
    
    name = "summarize"
    description = "Generate summary of crawled content"
    
    @staticmethod
    def execute(markdown: str, max_length: int = 500) -> str:
        """Execute summarization"""
        return ContentTools.summarize_content(markdown, max_length)


class ExtractImagesSkill:
    """Extract images from content"""
    
    name = "extract_images"
    description = "Extract all images from content"
    
    @staticmethod
    def execute(markdown: str) -> List[Dict[str, str]]:
        """Execute image extraction"""
        return ContentTools.extract_images(markdown)


class AnalyzeLinksSkill:
    """Analyze links"""
    
    name = "analyze_links"
    description = "Categorize and analyze links"
    
    @staticmethod
    def execute(links: List[str], base_url: str = "") -> Dict[str, Any]:
        """Execute link analysis"""
        return LinkTools.analyze_links(links, base_url)


class ExportSkill:
    """Export data in various formats"""
    
    name = "export"
    description = "Export data to JSON, CSV, or Markdown table"
    
    @staticmethod
    def execute(data: Any, format: str = "json") -> str:
        """Execute export"""
        if format == "json":
            return ExportTools.to_json(data)
        elif format == "csv":
            return ExportTools.to_csv(data)
        elif format == "table":
            return ExportTools.to_markdown_table(data)
        return str(data)


class FilterSkill:
    """Filter content"""
    
    name = "filter"
    description = "Filter content by extension or domain"
    
    @staticmethod
    def execute(links: List[str], filter_type: str = "extension", 
                extensions: List[str] = None, domains: List[str] = None) -> List[str]:
        """Execute filtering"""
        if filter_type == "extension" and extensions:
            return FilterTools.filter_by_extension(links, extensions)
        elif filter_type == "domain" and domains:
            return FilterTools.filter_by_domain(links, domains)
        return links


class DeduplicateSkill:
    """Remove duplicates"""
    
    name = "deduplicate"
    description = "Remove duplicate items"
    
    @staticmethod
    def execute(items: List[Any]) -> List[Any]:
        """Execute deduplication"""
        return FilterTools.remove_duplicates(items)


class ExtractCodeSkill:
    """Extract code blocks"""
    
    name = "extract_code"
    description = "Extract code blocks with language detection"
    
    @staticmethod
    def execute(markdown: str) -> List[Dict[str, str]]:
        """Execute code extraction"""
        return ContentTools.extract_code_blocks(markdown)


# Skill registry
AGENT_SKILLS = {
    "analyze_seo": AnalyzeSEOSkill,
    "summarize": SummarizeSkill,
    "extract_images": ExtractImagesSkill,
    "analyze_links": AnalyzeLinksSkill,
    "export": ExportSkill,
    "filter": FilterSkill,
    "deduplicate": DeduplicateSkill,
    "extract_code": ExtractCodeSkill,
}