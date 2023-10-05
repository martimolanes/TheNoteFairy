# request a url and return the html content (title only)
import requests
from bs4 import BeautifulSoup

def get_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.title.string
