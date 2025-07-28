from app.scrapers.perplexity_scraper import PerplexityScraper
import os

print('Testing Perplexity API integration...')
try:
    scraper = PerplexityScraper()
    print('PerplexityScraper initialized successfully')
    print('API key configured:', bool(os.getenv('PERPLEXITY_API_KEY')))
    
    print('Testing search functionality...')
    results = scraper.search_discussions("AI startup validation platform")
    print(f'Search returned {len(results)} results')
    if results:
        print('Sample result keys:', list(results[0].keys()))
        print('Sample content preview:', results[0].get('content', '')[:100])
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
