import requests
from flask import current_app
class NewsAPIClient:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key_index = 0

    def get_current_key(self):
        return self.api_keys[self.current_key_index]

    def switch_key(self):   
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    def make_request(self, endpoint, params):
        params['apiKey'] = self.get_current_key()
        response = requests.get(f"https://newsapi.org/v2/{endpoint}", params=params)
        
        if response.status_code == 429:  # Rate limit exceeded
            self.switch_key()
            params['apiKey'] = self.get_current_key()
            response = requests.get(f"https://newsapi.org/v2/{endpoint}", params=params)
        
        return response.json()
def get_search_results(query):
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'relevancy'
    }
    response = client.make_request('everything', params)
    articles = response.get('articles', [])

    results = []
    for article in articles:
        results.append({
            'title': article['title'],
            'url': article['url'],
            'description': article['description'],
            'date': article['publishedAt'],
            'image': article['urlToImage']
        })
    return results