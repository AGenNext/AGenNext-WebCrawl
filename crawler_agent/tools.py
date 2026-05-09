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


class ScreenshotTools:
    """Screenshot and Visual Capture Tools"""
    
    @staticmethod
    async def capture_page(url: str, driver=None) -> Dict[str, Any]:
        """
        Capture screenshot of a webpage
        
        Args:
            url: URL to capture
            driver: Optional Selenium WebDriver or Playwright page
            
        Returns:
            Dict with screenshot base64, dimensions, title
        """
        result = {
            "url": url,
            "screenshot": None,
            "title": None,
            "width": 0,
            "height": 0,
            "timestamp": None,
        }
        
        try:
            if driver:
                # Selenium-style
                driver.get(url)
                result["screenshot"] = driver.take_screenshot()
                result["title"] = driver.title
                window = driver.get_window_size()
                result["width"] = window["width"]
                result["height"] = window["height"]
            else:
                # Try Playwright
                import asyncio
                from playwright.async_api import async_playwright
                
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(url)
                    
                    # Get metadata before screenshot
                    result["title"] = await page.title()
                    view_size = await page.viewport_size
                    result["width"] = view_size["width"] if view_size else 0
                    result["height"] = view_size["height"] if view_size else 0
                    
                    # Capture
                    result["screenshot"] = await page.screenshot()
                    await browser.close()
            
            # Add timestamp
            from datetime import datetime
            result["timestamp"] = datetime.utcnow().isoformat()
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def capture_element(url: str, selector: str, driver=None) -> Dict[str, Any]:
        """Capture screenshot of specific element"""
        
        result = {
            "url": url,
            "selector": selector,
            "screenshot": None,
            "element_found": False,
        }
        
        try:
            import asyncio
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                
                # Check if element exists
                element = await page.query_selector(selector)
                if element:
                    result["element_found"] = True
                    result["screenshot"] = await element.screenshot()
                else:
                    result["error"] = f"Element not found: {selector}"
                
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def capture_full_page(url: str) -> Dict[str, Any]:
        """Capture full page screenshot (scrollable)"""
        
        result = {
            "url": url,
            "screenshot": None,
            "full_height": 0,
        }
        
        try:
            import asyncio
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Get full height
                await page.goto(url)
                await page.evaluate("() => document.body.scrollHeight")
                full_height = await page.evaluate("document.body.scrollHeight")
                result["full_height"] = full_height
                
                # Set viewport and capture
                await page.set_viewport_size({"width": 1920, "height": full_height})
                result["screenshot"] = await page.screenshot(full_page=True)
                
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def save_screenshot(screenshot_data: bytes, filepath: str) -> bool:
        """Save screenshot to file"""
        
        try:
            with open(filepath, "wb") as f:
                f.write(screenshot_data)
            return True
        except Exception:
            return False


class FormTools:
    """Form Filling and Interaction Tools"""
    
    @staticmethod
    async def fill_form(url: str, form_data: Dict[str, str], 
                    input_selectors: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Fill and submit a form
        
        Args:
            url: URL with form
            form_data: Dict of field names to values
            input_selectors: Optional custom selectors for fields
            
        Returns:
            Dict with success status, filled fields, response
        """
        result = {
            "url": url,
            "success": False,
            "filled_fields": [],
            "response_url": None,
            "errors": [],
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                
                # Auto-detect selectors if not provided
                if input_selectors is None:
                    input_selectors = {}
                
                # Fill fields
                for field_name, value in form_data.items():
                    # Try different selector strategies
                    selector = input_selectors.get(field_name)
                    
                    if selector:
                        # Use provided selector
                        try:
                            await page.fill(selector, value)
                            result["filled_fields"].append(field_name)
                        except Exception as e:
                            result["errors"].append(f"{field_name}: {str(e)}")
                    else:
                        # Auto-detect: try common patterns
                        strategies = [
                            f'name={field_name}',
                            f'id={field_name}',
                            f'[name="{field_name}"]',
                            f'#{field_name}',
                            f'input[placeholder*="{field_name}"]',
                            f'label:has-text("{field_name}") >> input',
                        ]
                        
                        for strategy in strategies:
                            try:
                                await page.fill(strategy, value)
                                result["filled_fields"].append(field_name)
                                break
                            except Exception:
                                continue
                
                # Submit form (try common submit buttons)
                submit_selector = 'button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Send")'
                try:
                    await page.click(submit_selector)
                    await page.wait_for_load_state()
                    result["response_url"] = page.url
                    result["success"] = True
                except Exception as e:
                    result["errors"].append(f"Submit: {str(e)}")
                
                await browser.close()
                
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    @staticmethod
    async def fill_input(url: str, selector: str, value: str) -> Dict[str, Any]:
        """Fill a specific input"""
        
        result = {
            "url": url,
            "selector": selector,
            "success": False,
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.fill(selector, value)
                result["success"] = True
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def click(url: str, selector: str) -> Dict[str, Any]:
        """Click an element"""
        
        result = {
            "url": url,
            "selector": selector,
            "success": False,
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.click(selector)
                await page.wait_for_load_state()
                result["success"] = True
                result["new_url"] = page.url
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def select_option(url: str, selector: str, value: str) -> Dict[str, Any]:
        """Select dropdown option"""
        
        result = {
            "url": url,
            "selector": selector,
            "value": value,
            "success": False,
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.select_option(selector, value)
                result["success"] = True
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def check_checkbox(url: str, selector: str, checked: bool = True) -> Dict[str, Any]:
        """Check or uncheck a checkbox"""
        
        result = {
            "url": url,
            "selector": selector,
            "checked": checked,
            "success": False,
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await page.goto(url)
                
                if checked:
                    await page.check(selector)
                else:
                    await page.uncheck(selector)
                
                result["success"] = True
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    async def type_text(url: str, selector: str, text: str, delay: int = 0) -> Dict[str, Any]:
        """Type text with optional delay between keystrokes"""
        
        result = {
            "url": url,
            "selector": selector,
            "text": text,
            "success": False,
        }
        
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                await page.type(selector, text, delay=delay)
                result["success"] = True
                await browser.close()
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def get_form_fields(html: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract form fields from HTML"""
        
        import re
        
        fields = {
            "inputs": [],
            "selects": [],
            "textareas": [],
            "checkboxes": [],
            "buttons": [],
        }
        
        # Input fields
        input_pattern = r'<input[^>]+>'
        for match in re.finditer(input_pattern, html):
            attrs = match.group()
            field = {}
            
            if 'name=' in attrs:
                field["name"] = re.search(r'name="([^"]+)"', attrs).group(1)
            if 'type=' in attrs:
                field["type"] = re.search(r'type="([^"]+)"', attrs).group(1)
            if 'id=' in attrs:
                field["id"] = re.search(r'id="([^"]+)"', attrs).group(1)
            if 'placeholder=' in attrs:
                field["placeholder"] = re.search(r'placeholder="([^"]+)"', attrs).group(1)
            
            fields["inputs"].append(field)
        
        # Select fields
        select_pattern = r'<select[^>]+name="([^"]+)"[^>]*>(.*?)</select>'
        for match in re.finditer(select_pattern, html, re.DOTALL):
            field = {"name": match.group(1), "options": []}
            options = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)', match.group(2))
            field["options"] = [{"value": v, "text": t} for v, t in options]
            fields["selects"].append(field)
        
        # Textareas
        textarea_pattern = r'<textarea[^>]+name="([^"]+)"[^>]*>'
        for match in re.finditer(textarea_pattern, html):
            fields["textareas"].append({"name": match.group(1)})
        
        return fields


# Tool registry for the agent
AGENT_TOOLS = {
    "seo": SEOTools,
    "content": ContentTools,
    "links": LinkTools,
    "export": ExportTools,
    "filter": FilterTools,
    "screenshot": ScreenshotTools,
    "form": FormTools,
}


class OCRTools:
    """OCR and Document Parsing Tools
    
    LiteParse: https://github.com/run-llama/liteparse
    TypeScript npm: npx @lupd/liteparse file.pdf
    
    Python alternatives:
    - EasyOCR: pip install easyocr
    - pdfplumber: pip install pdfplumber  
    """
    
    @staticmethod
    def parse_with_liteparse(file_path: str) -> Dict[str, Any]:
        """Parse document using LiteParse CLI (npx @lupd/liteparse)"""
        import subprocess
        import json
        import os
        
        result = {"success": False, "text": "", "pages": []}
        
        if not file_path or not os.path.exists(file_path):
            result["error"] = f"File not found: {file_path}"
            result["hint"] = "npm install -g @lupd/liteparse"
            return result
        
        try:
            output_file = file_path + ".json"
            # Use exact package from user: run-llama/liteparse
            cmd = ["npx", "@lupd/liteparse", file_path, "--output", output_file]
            
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if proc.returncode == 0 and os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    result["text"] = str(data)
                    result["success"] = True
                    result["parser"] = "@lupd/liteparse"
                os.unlink(output_file)
            else:
                result["error"] = proc.stderr or "LiteParse failed"
                result["hint"] = "npm install -g @lupd/liteparse"
        except FileNotFoundError:
            result["error"] = "npx not found - install Node.js"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def parse_with_easyocr(file_path: str = None,
                        image_data: bytes = None) -> Dict[str, Any]:
        """Parse image using EasyOCR (pip install easyocr)"""
        result = {"success": False, "text": [], "annotations": []}
        
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)
            
            if file_path:
                detections = reader.readtext(file_path)
            elif image_data:
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
                    f.write(image_data)
                    f.flush()
                    temp_path = f.name
                    detections = reader.readtext(temp_path)
                    os.unlink(temp_path)
            else:
                result["error"] = "No file path provided"
                return result
            
            text_lines = [d[1] for d in detections]
            result["text"] = text_lines
            result["annotations"] = [{"text": d[1], "confidence": d[2], "bbox": d[0]} for d in detections]
            result["success"] = True
            
        except ImportError:
            result["error"] = "easyocr not installed. pip install easyocr"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def extract_with_pytesseract(image_source: str) -> Dict[str, Any]:
        """Extract text using pytesseract"""
        result = {"success": False, "text": ""}
        
        try:
            import pytesseract
            from PIL import Image
            import requests
            from io import BytesIO
            
            if image_source.startswith('http'):
                response = requests.get(image_source)
                image = Image.open(BytesIO(response.content))
            elif image_source.startswith('data:'):
                import base64, io
                data = image_source.split(',')[1]
                image = Image.open(io.BytesIO(base64.b64decode(data)))
            else:
                image = Image.open(image_source)
            
            text = pytesseract.image_to_string(image)
            result["text"] = text.strip()
            result["success"] = True
            
        except ImportError:
            result["error"] = "pytesseract not installed. pip install pytesseract"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF using pdfplumber"""
        result = {"success": False, "pages": [], "page_count": 0}
        
        try:
            import pdfplumber
            
            with pdfplumber.open(file_path) as pdf:
                result["page_count"] = len(pdf.pages)
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    result["pages"].append({"page": i + 1, "text": text or ""})
            
            result["success"] = True
            
        except ImportError:
            result["error"] = "pdfplumber not installed. pip install pdfplumber"
        except Exception as e:
            result["error"] = str(e)
        
        return result


# Add OCR to tool registry
AGENT_TOOLS["ocr"] = OCRTools