import requests
import time
from typing import List, Dict
import re

class HackerNewsScraper:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self.hn_url = "https://news.ycombinator.com"
        self.rate_limit_delay = 1
    
    def search_discussions(self, query: str) -> List[Dict]:
        try:
            search_results = self._search_algolia(query)
            
            results = []
            for item in search_results[:15]:
                if item.get("story_text") or item.get("comment_text"):
                    result = {
                        "source": "hackernews",
                        "source_url": f"{self.hn_url}/item?id={item.get('objectID', '')}",
                        "title": item.get("story_title", item.get("title", "")),
                        "content": self._clean_text(item.get("story_text", item.get("comment_text", ""))),
                        "score": item.get("points", 0),
                        "num_comments": item.get("num_comments", 0),
                        "created_at": item.get("created_at", "")
                    }
                    
                    if result["content"] or result["title"]:
                        results.append(result)
                
                time.sleep(0.1)
            
            return results
            
        except Exception as e:
            print(f"Error scraping Hacker News: {e}")
            return []
    
    def _search_algolia(self, query: str) -> List[Dict]:
        algolia_url = "https://hn.algolia.com/api/v1/search"
        params = {
            "query": query,
            "tags": "story,comment",
            "hitsPerPage": 20
        }
        
        try:
            response = requests.get(algolia_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("hits", [])
            
        except Exception as e:
            print(f"Error with Algolia search: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
