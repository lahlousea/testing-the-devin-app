import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re
import time

class BlogScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "StartupValidationBot/1.0 (Educational Research)"
        }
        self.rate_limit_delay = 2
        
        self.blog_sources = [
            "https://techcrunch.com",
            "https://medium.com",
            "https://www.producthunt.com"
        ]
    
    def search_discussions(self, query: str) -> List[Dict]:
        all_results = []
        
        search_results = self._search_google_for_blogs(query)
        
        for result in search_results[:10]:
            try:
                content = self._scrape_article(result["url"])
                if content:
                    result["content"] = content
                    all_results.append(result)
                
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"Error scraping {result['url']}: {e}")
                continue
        
        return all_results
    
    def _search_google_for_blogs(self, query: str) -> List[Dict]:
        results = []
        
        mock_results = [
            {
                "source": "techcrunch",
                "source_url": "https://techcrunch.com/startup-validation-example",
                "title": f"Startup Validation: {query} Market Analysis",
                "content": f"Recent analysis shows that {query} represents a growing market opportunity. Industry experts suggest that startups in this space should focus on customer validation and product-market fit."
            },
            {
                "source": "medium",
                "source_url": "https://medium.com/startup-validation-example",
                "title": f"How to Validate Your {query} Startup Idea",
                "content": f"Validating a {query} startup requires understanding customer pain points and market demand. Successful entrepreneurs recommend starting with customer interviews and MVP testing."
            },
            {
                "source": "producthunt",
                "source_url": "https://producthunt.com/startup-validation-example",
                "title": f"{query} Tools and Resources",
                "content": f"The {query} space has seen significant innovation recently. Users are looking for solutions that provide better value and user experience compared to existing alternatives."
            }
        ]
        
        return mock_results
    
    def _scrape_article(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.decompose()
            
            content_selectors = [
                "article",
                ".post-content",
                ".entry-content",
                ".content",
                "main"
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text()
                    break
            
            if not content:
                content = soup.get_text()
            
            return self._clean_text(content)
            
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()[:1000]
