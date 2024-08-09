from flask import Blueprint, jsonify, request, current_app, render_template
from app.utils import NewsAPIClient, get_search_results,get_weather_data




# recommendation_bp = Blueprint('recommendation', __name__)
def trending_news():
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    
    # Get trending news
    trending_params = {
        'q': 'trending',
        'language': 'en',
        'sortBy': 'popularity',
        'pageSize': 5
    }
    trending_response = client.make_request('everything', trending_params)
    trending_articles = trending_response.get('articles', [])
    
    trending_news = []
    for article in trending_articles:
        if article['source']['name'] != '[Removed]':
            trending_news.append({
                'title': article['title'],
                'url': article['url'],
                'image': article.get('urlToImage', ''),
                'source': article['source']['name'],
                'publishedAt': article['publishedAt']
            })
    return trending_news

def top_story():
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    
    # Get top story
    top_story_params = {
        'q': 'top story',
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 1
    }
    top_story_response = client.make_request('everything', top_story_params)
    top_story_articles = top_story_response.get('articles', [])
    
    if top_story_articles:
        top_story = top_story_articles[0]
        if top_story['source']['name'] != '[Removed]':
            story = {
                'title': top_story['title'],
                'url': top_story['url'],
                'image': top_story.get('urlToImage', ''),
                'source': top_story['source']['name'],
                'publishedAt': top_story['publishedAt'],
                'description': top_story.get('description', '')
            }
            return story
    return None

def get_top_story():
    return top_story()

def get_trending_news():
    return trending_news()

def popular_news():
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    
    # Get popular news
    popular_params = {
        'language': 'en',
        'sortBy': 'popularity',
        'pageSize': 6,
        'q': 'popular'  # Add a query to ensure we get results
    }
    popular_response = client.make_request('everything', popular_params)
    popular_articles = popular_response.get('articles', [])
    
    popular_news = []
    for article in popular_articles:
        if article['source']['name'] != '[Removed]':
            popular_news.append({
                'title': article['title'],
                'url': article['url'],
                # 'image': article.get('urlToImage', ''),  # Add image URL, use empty string if not available
                'source': article['source']['name'],
                'publishedAt': article['publishedAt']
            })
    
    return popular_news

def get_popular_news():
    return popular_news()

# @recommendation_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    query = request.args.get('query', 'technology')  # Default to 'technology' if no query provided
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 10  # Limit to 10 recommendations
    }
    
    response = client.make_request('everything', params)
    articles = response.get('articles', [])
    
    recommendations = []
    for article in articles:
        recommendations.append({
            'title': article['title'],
            'url': article['url'],
            'description': article['description'],
            'publishedAt': article['publishedAt'],
            'source': article['source']['name']
        })
    
    return jsonify(recommendations)

# @recommendation_bp.route('/api/trending', methods=['GET'])
def get_trending():
    client = NewsAPIClient(current_app.config['NEWSAPI_KEYS'])
    
    params = {
        'country': 'us',  # You can make this dynamic based on user's location
        'category': 'general',
        'pageSize': 5  # Limit to 5 trending articles
    }
    
    response = client.make_request('top-headlines', params)
    articles = response.get('articles', [])
    
    trending = []
    for article in articles:
        trending.append({
            'title': article['title'],
            'url': article['url'],
            'source': article['source']['name']
        })
    
    return jsonify(trending)

# @recommendation_bp.route('/api/search', methods=['GET'])
def search_news():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    results = get_search_results(query)
    return jsonify(results)