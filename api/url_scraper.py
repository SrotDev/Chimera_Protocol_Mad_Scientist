"""
URL Content Scraper Service
Uses Playwright for headless browser scraping to handle JavaScript-rendered content.
Supports ChatGPT, Notion, Google Docs, and other dynamic sites.
"""
import asyncio
import re
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Maximum content length (characters)
MAX_CONTENT_LENGTH = 50000

# Timeout for page load (milliseconds)
PAGE_TIMEOUT = 60000

# Wait time for dynamic content to load (milliseconds)
DYNAMIC_CONTENT_WAIT = 3000


def detect_url_type(url: str) -> str:
    """Detect the type of URL to apply appropriate scraping strategy."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    if 'chat.openai.com' in domain or 'chatgpt.com' in domain:
        return 'chatgpt'
    elif 'notion.so' in domain or 'notion.site' in domain:
        return 'notion'
    elif 'docs.google.com' in domain:
        return 'google_docs'
    elif 'gemini.google.com' in domain:
        return 'gemini'
    elif 'chat.deepseek.com' in domain:
        return 'deepseek'
    elif 'claude.ai' in domain:
        return 'claude'
    elif 'poe.com' in domain:
        return 'poe'
    elif 'github.com' in domain:
        return 'github'
    elif 'medium.com' in domain:
        return 'medium'
    else:
        return 'generic'


def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    if not text:
        return ''
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    return text.strip()


async def scrape_with_playwright(url: str, url_type: str) -> dict:
    """
    Scrape content using Playwright headless browser.
    This handles JavaScript-rendered content properly.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return {
            'success': False,
            'error': 'Playwright not installed. Run: pip install playwright && playwright install chromium'
        }
    
    browser = None
    try:
        async with async_playwright() as p:
            # Launch headless browser
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # Create context with realistic viewport
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Navigate to URL
            await page.goto(url, wait_until='networkidle', timeout=PAGE_TIMEOUT)
            
            # Wait for dynamic content based on URL type
            await handle_dynamic_content(page, url_type)
            
            # Get page content
            html_content = await page.content()
            title = await page.title()
            
            # Extract text content
            content = await extract_content(page, html_content, url_type)
            
            await browser.close()
            
            if len(content) < 50:
                return {
                    'success': False,
                    'error': 'Could not extract meaningful content. The page might require login or have restricted access.'
                }
            
            # Truncate if too long
            if len(content) > MAX_CONTENT_LENGTH:
                content = content[:MAX_CONTENT_LENGTH] + '\n\n[Content truncated due to length]'
            
            return {
                'success': True,
                'title': clean_text(title) or 'Imported Content',
                'content': content,
                'type': url_type,
                'source_url': url
            }
            
    except Exception as e:
        logger.error(f"Playwright scraping error for {url}: {str(e)}")
        if browser:
            try:
                await browser.close()
            except:
                pass
        return {
            'success': False,
            'error': f'Failed to scrape page: {str(e)}'
        }


async def handle_dynamic_content(page, url_type: str):
    """Handle dynamic content loading based on URL type."""
    try:
        if url_type == 'chatgpt':
            # Wait for ChatGPT conversation to load
            await page.wait_for_selector('[data-message-author-role]', timeout=10000)
            # Scroll to load all messages
            await auto_scroll(page)
            
        elif url_type == 'notion':
            # Wait for Notion content blocks
            await page.wait_for_selector('.notion-page-content', timeout=10000)
            await auto_scroll(page)
            
        elif url_type == 'google_docs':
            # Wait for Google Docs content
            await page.wait_for_selector('.kix-page', timeout=10000)
            
        elif url_type in ['gemini', 'deepseek', 'claude', 'poe']:
            # Wait for chat messages
            await page.wait_for_timeout(DYNAMIC_CONTENT_WAIT)
            await auto_scroll(page)
            
        else:
            # Generic wait for content
            await page.wait_for_timeout(2000)
            
    except Exception as e:
        logger.warning(f"Dynamic content handling warning: {str(e)}")
        # Continue anyway, we might still get some content


async def auto_scroll(page, max_scrolls: int = 10):
    """Scroll through the page to load lazy-loaded content."""
    try:
        for _ in range(max_scrolls):
            # Scroll down
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await page.wait_for_timeout(500)
            
            # Check if we've reached the bottom
            at_bottom = await page.evaluate('''
                () => window.innerHeight + window.scrollY >= document.body.scrollHeight - 100
            ''')
            if at_bottom:
                break
        
        # Scroll back to top
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(500)
        
    except Exception as e:
        logger.warning(f"Auto-scroll warning: {str(e)}")


async def extract_content(page, html_content: str, url_type: str) -> str:
    """Extract text content based on URL type."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']):
        element.decompose()
    
    if url_type == 'chatgpt':
        return extract_chatgpt_content(soup, page)
    elif url_type == 'notion':
        return extract_notion_content(soup)
    elif url_type == 'google_docs':
        return extract_google_docs_content(soup)
    elif url_type in ['gemini', 'deepseek', 'claude', 'poe']:
        return extract_chat_content(soup, url_type)
    else:
        return extract_generic_content(soup)


def extract_chatgpt_content(soup: BeautifulSoup, page=None) -> str:
    """Extract content from ChatGPT shared conversation."""
    messages = []
    
    # Try multiple selectors for ChatGPT messages
    selectors = [
        '[data-message-author-role]',
        '.markdown',
        '.text-base',
        '[class*="message"]',
        '.prose'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            for elem in elements:
                text = clean_text(elem.get_text())
                if text and len(text) > 10 and text not in messages:
                    messages.append(text)
            if messages:
                break
    
    if messages:
        return '\n\n---\n\n'.join(messages)
    
    # Fallback: get main content
    main = soup.find('main') or soup.find('article') or soup.body
    return clean_text(main.get_text()) if main else ''


def extract_notion_content(soup: BeautifulSoup) -> str:
    """Extract content from Notion page."""
    content_parts = []
    
    # Try Notion-specific selectors
    selectors = [
        '.notion-page-content',
        '[class*="notion"]',
        '.layout-content',
        'article',
        'main'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            for elem in elements:
                text = clean_text(elem.get_text())
                if text and len(text) > 20:
                    content_parts.append(text)
            if content_parts:
                break
    
    if content_parts:
        return '\n\n'.join(content_parts)
    
    return clean_text(soup.get_text())


def extract_google_docs_content(soup: BeautifulSoup) -> str:
    """Extract content from Google Docs."""
    # Google Docs specific selectors
    selectors = [
        '.kix-page',
        '.doc-content',
        '#contents',
        '.docs-texteventtarget-iframe'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            content = '\n\n'.join([clean_text(e.get_text()) for e in elements])
            if content:
                return content
    
    return clean_text(soup.get_text())


def extract_chat_content(soup: BeautifulSoup, url_type: str) -> str:
    """Extract content from various chat interfaces."""
    messages = []
    
    # Common chat message selectors
    selectors = [
        '[class*="message"]',
        '[class*="chat"]',
        '[class*="conversation"]',
        '.markdown',
        '.prose',
        'article'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            for elem in elements:
                text = clean_text(elem.get_text())
                if text and len(text) > 10:
                    messages.append(text)
            if messages:
                break
    
    if messages:
        return '\n\n---\n\n'.join(messages)
    
    return clean_text(soup.get_text())


def extract_generic_content(soup: BeautifulSoup) -> str:
    """Extract content from generic webpage."""
    # Try to find main content area
    main_selectors = [
        'main',
        'article',
        '[role="main"]',
        '.content',
        '.post-content',
        '.entry-content',
        '#content'
    ]
    
    for selector in main_selectors:
        element = soup.select_one(selector)
        if element:
            text = clean_text(element.get_text())
            if len(text) > 100:
                return text
    
    # Fallback to body
    return clean_text(soup.body.get_text()) if soup.body else ''


def scrape_url(url: str) -> dict:
    """
    Main entry point for URL scraping.
    Uses Playwright for JavaScript-rendered content.
    """
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {
                'success': False,
                'error': 'Invalid URL format'
            }
        
        if parsed.scheme not in ['http', 'https']:
            return {
                'success': False,
                'error': 'Only HTTP and HTTPS URLs are supported'
            }
        
        url_type = detect_url_type(url)
        
        # Run async scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(scrape_with_playwright(url, url_type))
        finally:
            loop.close()
        
        return result
        
    except Exception as e:
        logger.error(f"Error in scrape_url: {str(e)}")
        return {
            'success': False,
            'error': f'Scraping failed: {str(e)}'
        }


def summarize_content(content: str, title: str, api_key: str = None) -> str:
    """
    Summarize the scraped content using an LLM.
    """
    from .llm_router import call_llm
    
    # Create a prompt for summarization
    prompt = f"""Please summarize the following content from "{title}". 
Create a concise but comprehensive summary that captures the key points, main ideas, and important details.
Format the summary in a clear, readable way with bullet points for key takeaways.

Content to summarize:
---
{content[:15000]}  
---

Summary:"""
    
    try:
        response = call_llm('echo', prompt, '', api_key)
        
        if response.get('status') == 'success':
            return response.get('reply', content[:2000])
        else:
            return content[:2000] + '...' if len(content) > 2000 else content
            
    except Exception as e:
        logger.error(f"Error summarizing content: {str(e)}")
        return content[:2000] + '...' if len(content) > 2000 else content
