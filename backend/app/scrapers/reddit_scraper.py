import requests
import time
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class RedditScraper:
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            "User-Agent": "StartupValidationBot/1.0 (Educational Research)"
        }
        self.rate_limit_delay = 2
    
    def search_discussions(self, query: str, subreddits: List[str] | None = None) -> List[Dict]:
        if subreddits is None:
            subreddits = ["entrepreneur", "startups", "business", "smallbusiness", "SaaS"]
        
        all_results = []
        
        for subreddit in subreddits:
            try:
                results = self._search_subreddit(query, subreddit)
                all_results.extend(results)
                time.sleep(self.rate_limit_delay)
            except Exception as e:
                print(f"Error scraping r/{subreddit}: {e}")
                continue
        
        return all_results[:20]
    
    def _search_subreddit(self, query: str, subreddit: str) -> List[Dict]:
        search_url = f"{self.base_url}/r/{subreddit}/search.json"
        params = {
            "q": query,
            "restrict_sr": "1",
            "sort": "relevance",
            "limit": 10
        }
        
        try:
            response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get("data", {}).get("children", [])
            
            results = []
            for post in posts:
                post_data = post.get("data", {})
                
                result = {
                    "source": f"reddit_r_{subreddit}",
                    "source_url": f"{self.base_url}{post_data.get('permalink', '')}",
                    "title": post_data.get("title", ""),
                    "content": self._clean_text(post_data.get("selftext", "")),
                    "score": post_data.get("score", 0),
                    "num_comments": post_data.get("num_comments", 0),
                    "created_utc": post_data.get("created_utc", 0)
                }
                
                if result["content"] or result["title"]:
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error searching r/{subreddit}: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
