import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
from urllib.parse import urljoin
from config import KARNATAKA_URL, DATA_DIR

def scrape_karnataka():
    response = requests.get(KARNATAKA_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate "SERVICES AND SCHEMES" header element
    service_header = None
    for header in soup.find_all(['h2', 'h3', 'div']):
        if header.text.strip().upper() == "SERVICES AND SCHEMES":
            service_header = header
            break

    if service_header is None:
        raise Exception("Could not find Services and Schemes header")

    parent_div = service_header.find_parent('div')

    # Find all anchor tags under this parent container
    scheme_links = parent_div.find_all('a', href=True)

    scheme_list = []
    for a in scheme_links:
        name = a.get_text(strip=True)
        href = urljoin(KARNATAKA_URL, a['href'])
        scheme_list.append({'Scheme Name': f'<a href="{href}" target="_blank">{name}</a>'})

    # Fallback if no anchor links found, get list items text
    if not scheme_list:
        lis = parent_div.find_all('li')
        for li in lis:
            scheme_list.append({'Scheme Name': li.get_text(strip=True)})

    df = pd.DataFrame(scheme_list)
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f'karnataka_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)
    print(f"Karnataka schemes scraped to {filename}")

if __name__ == "__main__":
    scrape_karnataka()

