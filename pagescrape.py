from typing import Dict
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def pagescrape(url: str , topic: str = None) -> Dict[str, str]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', class_='entry-content')
    sf_contents = content.findAll('div', class_='sf-section')
    
    if topic is None: 
        filtered_sf_content = [
            item for item in sf_contents
            if item.h2 is not None and item.table is not None
        ]
    else:
        filtered_sf_content = [
            item for item in sf_contents
            if item.h2 is not None and item.h2.text == topic
        ]

    tables = [item.table for item in filtered_sf_content]
    links = {}
    for table in tables:
        try:
            hrefs = {link.text.strip().replace(" ", '-'): link["href"] for link in table.findAll('a')}
            links.update(hrefs)
        except Exception:
            pass
    return links
