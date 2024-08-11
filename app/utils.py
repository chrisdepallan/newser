import requests, random
from datetime import datetime
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask import current_app

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def get_weather_data():
    location = get_location()
    city = location.get("city")
    
    api_key = current_app.config['WEATHERAPI_KEY']
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        current_date = datetime.now()
        weather_data = {
            "temperature": round(data["current"]["temp_c"]),
            "icon_url": f"https:{data['current']['condition']['icon']}",
            "city": data["location"]["name"],
            "date": current_date.strftime("%b %d, %Y"),
            "weekday": current_date.strftime("%A")
        }

        return weather_data

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def setup_cloudinary():
    cloudinary.config(
        cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=current_app.config['CLOUDINARY_API_KEY'],
        api_secret=current_app.config['CLOUDINARY_API_SECRET']
    )

def upload_image(image_file):
    setup_cloudinary()
    result = cloudinary.uploader.upload(image_file)
    return result['public_id']

def get_image_url(public_id):
    setup_cloudinary()
    return cloudinary_url(public_id, width=800, height=800, crop="fill")[0]

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


def generate_avatar_url(style, seed=None, hair=None, flip=None):
    base_url = f'https://api.dicebear.com/9.x/{style}/svg'
    params = []
    
    if seed:
        params.append(f'seed={seed}')
    else:
        # Generate a random seed if not provided
        params.append(f'seed={random.randint(1, 1000000)}')
    
    if hair:
        params.append(f'hair={",".join(hair)}')
    
    if flip is not None:
        params.append(f'flip={str(flip).lower()}')
    
    return f'{base_url}?{"&".join(params)}'

def datetime_filter(value, format="%B %d, %Y"):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime(format)
# from app import bcrypt, collection_login_credentials




# Usage in your login route:
# from app.utils import get_weather_data
# weather_data = get_weather_data(YOUR_API_KEY, user_city)
# Add weather_data to session or pass it to the template