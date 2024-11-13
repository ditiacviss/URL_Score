from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
import requests
# X-Frame-Options - SAMEORIGIN/DENY, None means allows  header is only useful when the HTTP response where it is included has something to interact with (e.g. links, buttons).

def get_security_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        return [
            headers.get('X-Frame-Options', 'None'),
            headers.get('Strict-Transport-Security', 'None'),
            headers.get('Content-Security-Policy', 'None'),
            headers.get('X-XSS-Protection', 'None'),
            headers.get('X-Content-Type-Options', 'None'),
            headers.get('X-DNS-Prefetch-Control', 'None'),
            headers.get('Cross-Origin-Embedder-Policy', 'None'),
            headers.get('Cross-Origin-Opener-PolicyNone', 'None'),
            headers.get('Referrer-Policy', 'None'),
            headers.get('X-Powered-By', 'None'),
            headers.get('Set-Cookie', 'None'),
            headers.get('Content-Type', 'None')
        ]
    except requests.exceptions.RequestException:
        return None
def get_meta_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = soup.find_all('meta')
        return [{tag.get('name'): tag.get('content') for tag in meta_tags if tag.get('name')}]
    except:
        return None

def get_content_ratio(url):
    try:
        response = requests.get(url)
        content_length = len(response.text)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        visible_content_length = len(text)
        return visible_content_length / content_length if content_length > 0 else 0
    except:
        return None
