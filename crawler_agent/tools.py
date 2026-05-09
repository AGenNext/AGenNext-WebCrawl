"""Tools and skills for the Web Crawling Agent"""
from typing import List, Dict, Any, Optional
import json
import re
from urllib.parse import urlparse


class SEOTools:
    """SEO Analysis Tools"""
    
    @staticmethod
    def extract_meta_tags(html: str) -> Dict[str, str]:
        """Extract SEO meta tags from HTML"""
        meta_tags = {}
        
        patterns = {
            "title": r'<title[^>]*>([^<]+)</title>',
            "description": r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']',
            "keywords": r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']',
            "author": r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']',
            "robots": r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']+)["\']',
            "canonical": r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                meta_tags[key] = match.group(1).strip()
        
        return meta_tags
    
    @staticmethod
    def analyze_readability(markdown: str) -> Dict[str, Any]:
        """Analyze content readability"""
        words = markdown.split()
        sentences = re.split(r'[.!?]+', markdown)
        
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "readability_score": "easy" if avg_sentence_length < 20 else "medium" if avg_sentence_length < 30 else "hard"
        }
    
    @staticmethod
    def extract_headings(markdown: str) -> Dict[str, List[str]]:
        """Extract all headings for structure analysis"""
        headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
        
        for level in range(1, 7):
            pattern = r'\n' + '#' * level + r' ([^\n]+)'
            matches = re.findall(pattern, markdown)
            headings[f"h{level}"] = matches
        
        return headings


class ContentTools:
    """Content Processing Tools"""
    
    @staticmethod
    def summarize_content(markdown: str, max_length: int = 500) -> str:
        """Generate content summary"""
        # Remove markdown syntax
        text = re.sub(r'[#*`\[\]()_~-]', '', markdown)
        text = re.sub(r'\n+', '\n', text)
        
        # Get first N characters
        if len(text) <= max_length:
            return text.strip()
        
        # Find a good break point
        summary = text[:max_length]
        last_break = summary.rfind('. ')
        
        if last_break > max_length * 0.5:
            return summary[:last_break+1].strip()
        
        return summary.strip() + "..."
    
    @staticmethod
    def extract_images(markdown: str) -> List[Dict[str, str]]:
        """Extract all images from markdown"""
        images = []
        
        # Markdown images ![alt](url)
        md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(md_pattern, markdown):
            images.append({
                "alt": match.group(1),
                "url": match.group(2),
                "type": "markdown"
            })
        
        # HTML images <img src="...">
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(html_pattern, markdown):
            images.append({
                "alt": "",
                "url": match.group(1),
                "type": "html"
            })
        
        return images
    
    @staticmethod
    def extract_code_blocks(markdown: str) -> List[Dict[str, str]]:
        """Extract code blocks with language detection"""
        code_blocks = []
        
        # Fenced code blocks
        pattern = r'```(\w*)\n(.*?)```'
        for match in re.finditer(pattern, markdown, re.DOTALL):
            code_blocks.append({
                "language": match.group(1) or "text",
                "code": match.group(2).strip()
            })
        
        return code_blocks


class LinkTools:
    """Link Analysis Tools"""
    
    @staticmethod
    def analyze_links(links: List[str], base_url: str = "") -> Dict[str, Any]:
        """Analyze collected links"""
        internal = []
        external = []
        social = []
        
        social_domains = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "youtube.com", "github.com"]
        
        for link in links:
            parsed = urlparse(link)
            
            if parsed.netloc in ["", base_url] or (not parsed.netloc and base_url):
                internal.append(link)
            elif any(domain in parsed.netloc for domain in social_domains):
                social.append(link)
            else:
                external.append(link)
        
        return {
            "total": len(links),
            "internal": internal,
            "external": external,
            "social": social,
            "internal_count": len(internal),
            "external_count": len(external),
            "social_count": len(social),
        }
    
    @staticmethod
    def extract_sitemap(url: str, xml_content: str) -> List[str]:
        """Extract URLs from sitemap XML"""
        urls = []
        
        # Standard sitemap
        loc_pattern = r'<loc>([^<]+)</loc>'
        urls = re.findall(loc_pattern, xml_content)
        
        # Sitemap index
        if not urls:
            loc_pattern = r'<loc>([^<]+)</loc>'
            urls = re.findall(loc_pattern, xml_content)
        
        return urls


class ExportTools:
    """Data Export Tools"""
    
    @staticmethod
    def to_json(data: Any, pretty: bool = True) -> str:
        """Export to JSON"""
        return json.dumps(data, indent=2 if pretty else None, ensure_ascii=False)
    
    @staticmethod
    def to_csv(data: List[Dict], fields: Optional[List[str]] = None) -> str:
        """Export to CSV"""
        if not data:
            return ""
        
        # Get fields
        if fields is None:
            fields = list(data[0].keys())
        
        # Header
        csv = ",".join(fields) + "\n"
        
        # Rows
        for row in data:
            values = [str(row.get(f, "")) for f in fields]
            csv += ",".join([f'"{v}"' for v in values]) + "\n"
        
        return csv
    
    @staticmethod
    def to_markdown_table(data: List[Dict]) -> str:
        """Export to Markdown table"""
        if not data:
            return ""
        
        fields = list(data[0].keys())
        
        # Header
        md = "| " + " | ".join(fields) + " |\n"
        
        # Separator
        md += "| " + " | ".join(["---"] * len(fields)) + " |\n"
        
        # Rows
        for row in data:
            values = [str(row.get(f, "")) for f in fields]
            md += "| " + " | ".join(values) + " |\n"
        
        return md


class FilterTools:
    """Content Filtering Tools"""
    
    @staticmethod
    def filter_by_extension(links: List[str], extensions: List[str]) -> List[str]:
        """Filter links by file extension"""
        return [l for l in links if any(l.lower().endswith(ext) for ext in extensions)]
    
    @staticmethod
    def filter_by_domain(links: List[str], domains: List[str]) -> List[str]:
        """Filter links by domain"""
        return [l for l in links if any(domain in urlparse(l).netloc for domain in domains)]
    
    @staticmethod
    def remove_duplicates(items: List[Any]) -> List[Any]:
        """Remove duplicates while preserving order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result


# Tool registry for the agent
AGENT_TOOLS = {
    "seo": SEOTools,
    "content": ContentTools,
    "links": LinkTools,
    "export": ExportTools,
    "filter": FilterTools,
}