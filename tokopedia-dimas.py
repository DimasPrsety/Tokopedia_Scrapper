import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.tokopedia.com/search?st=&q=nugget%20ikan&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='


# send a get request to the url
headers = {
    'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)

