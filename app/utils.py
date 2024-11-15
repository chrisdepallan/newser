import requests, random
from datetime import datetime
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os,json
from flask import flash



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
        # params['country'] = 'in'  # Add this line to filter news from India
        
        response = requests.get(f"https://newsapi.org/v2/{endpoint}", params=params)
        print(response.url)
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

#  Mail sending function

def send_mass_email(emails, subject, quill_content, image_files=None):
    # Configure email settings
    smtp_server = current_app.config['MAIL_SERVER']
    smtp_port = current_app.config['MAIL_PORT']
    sender_email = current_app.config['MAIL_DEFAULT_SENDER']
    password = current_app.config['MAIL_PASSWORD']

    # Connect to SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)

    # Send emails
    for recipient_email in emails:
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Add Quill.js content as HTML body to email
        message.attach(MIMEText(quill_content, 'html'))

        # Attach images if provided
        # if image_files:
        #     for i, image_file in enumerate(image_files, start=1):
        #         with open(image_file, 'rb') as img:
        #             img_data = img.read()
        #             image = MIMEImage(img_data, name=os.path.basename(image_file))
        #             image.add_header('Content-ID', f'<image{i}>')
        #             message.attach(image)

        # Send email
        server.send_message(message)
        print(f"Email sent to {recipient_email}")

    # Close the SMTP server connection
    server.quit()

    print("All emails sent successfully.")

def get_article_details(article_url):
    """
    Fetch detailed information about an article using its URL through direct web scraping.
    
    Args:
        article_url (str): The URL of the article to fetch details for
        
    Returns:
        dict: Article details including title, content, author, etc.
    """
    try:
        # Enhanced headers to better mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        # Fetch the article page
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Enhanced title extraction
        title = (
            soup.find('h1', class_=['article-headline', 'story-headline']) or  # Common news sites
            soup.find('h1', {'data-component': 'headline'}) or  # BBC specific
            soup.find('h1') or 
            soup.find('title')
        )
        title = title.text.strip() if title else ''
        
        # Enhanced content extraction for BBC and other sites
        article_content = ''
        content_candidates = soup.find_all(['article', 'div'], class_=[
            'article-content', 'content', 'story-content', 
            'article__body-content', 'story-body',  # BBC specific
            'article-body', 'main-content'
        ])
        if content_candidates:
            # Remove unwanted elements
            for elem in content_candidates[0].find_all(['script', 'style', 'nav']):
                elem.decompose()
            article_content = ' '.join(p.text.strip() for p in content_candidates[0].find_all('p'))
        
        # Enhanced author extraction
        author = ''
        author_candidates = soup.find_all(['a', 'span', 'div'], class_=[
            'author', 'byline', 'article-author',
            'author-name', 'article__author'  # BBC specific
        ])
        if author_candidates:
            author = author_candidates[0].get_text(strip=True)
        
        # Try to find the publish date
        publish_date = ''
        date_candidates = soup.find_all(['time', 'span', 'div'], class_=['date', 'published', 'timestamp'])
        if date_candidates:
            publish_date = date_candidates[0].get_text(strip=True)
        
        # Try to find the main image
        image_url = ''
        image = soup.find('meta', property='og:image') or soup.find('meta', property='twitter:image')
        if image:
            image_url = image.get('content', '')
        
        # Extract keywords/tags from meta tags
        tags = set()
        keywords_meta = soup.find('meta', {'name': 'keywords'})
        if keywords_meta:
            tags.update(tag.strip().lower() for tag in keywords_meta.get('content', '').split(','))
        
        # Add some words from title as tags
        if title:
            title_words = [word.lower() for word in title.split() if len(word) > 3]
            tags.update(title_words[:5])  # Add up to 5 words from title as tags
        
        return {
            'title': title,
            'url': article_url,
            'content': article_content[:1000] if article_content else '',  # Limit content length
            'author': author,
            'publishedAt': publish_date,
            'urlToImage': image_url,
            'tags': list(tags),
            'relatedArticles': []  # Empty list since we can't easily get related articles without an API
        }
        
    except Exception as e:
        print(f"Error fetching article details: {e}")
        return {}