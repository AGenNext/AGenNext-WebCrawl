"""Examples for crawling with different modes"""
import asyncio
from crawler_agent import CrawlAgent, quick_crawl


async def example_single_page():
    """Example: Single page crawl"""
    print("\n=== Single Page Crawl ===")
    
    result = await quick_crawl(
        url="https://example.com",
        mode="single",
        provider="crawl4ai",
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Pages crawled: {result.get('total_pages')}")
    
    if result.get("crawled_pages"):
        page = result["crawled_pages"][0]
        print(f"URL: {page.get('url')}")
        print(f"Title: {page.get('metadata', {}).get('title')}")
        print(f"Links found: {len(page.get('links', []))}")
    
    return result


async def example_depth_crawl():
    """Example: Depth-based crawl"""
    print("\n=== Depth Crawl ===")
    
    agent = CrawlAgent(provider="crawl4ai")
    
    result = await agent.crawl(
        url="https://example.com",
        mode="depth",
        depth=2,
        max_pages=5,
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Pages crawled: {result.get('total_pages')}")
    print(f"Mode: {result.get('mode')}")
    
    return result


async def example_deep_crawl():
    """Example: Deep crawl (limited for demo)"""
    print("\n=== Deep Crawl ===")
    
    agent = CrawlAgent(provider="crawl4ai")
    
    result = await agent.crawl(
        url="https://example.com",
        mode="deep",
        max_urls=10,  # Limit to prevent infinite
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Pages crawled: {result.get('total_pages')}")
    print(f"Max URLs: 10")
    
    return result


async def example_knowledge():
    """Example: Knowledge graph extraction"""
    print("\n=== Knowledge Graph ===")
    
    agent = CrawlAgent(provider="crawl4ai")
    
    result = await agent.crawl(
        url="https://example.com",
        mode="knowledge",
        depth=1,
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Knowledge Graph: {result.get('knowledge_graph', {}).get('entities', [])[:3]}")
    
    return result


async def main():
    """Run all examples"""
    
    print("Web Crawling Agent Examples")
    print("=" * 40)
    
    # Run single page example
    await example_single_page()
    
    # Uncomment to run more examples
    # await example_depth_crawl()
    # await example_deep_crawl()
    # await example_knowledge()
    
    print("\n=== All examples completed! ===")


if __name__ == "__main__":
    asyncio.run(main())