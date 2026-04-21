import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
from urllib.parse import urljoin
from config import CENTRAL_URL, DATA_DIR

def scrape_central():
    response = requests.get(CENTRAL_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []

    for row in rows:
        cols = []
        for td in row.find_all(['td', 'th']):
            a_tag = td.find('a')
            if a_tag and a_tag.get('href'):
                href = urljoin(CENTRAL_URL, a_tag['href'])
                text = a_tag.get_text(strip=True)
                link_html = f'<a href="{href}" target="_blank">{text}</a>'
                cols.append(link_html)
            else:
                cols.append(td.get_text(strip=True))
        data.append(cols)

    df = pd.DataFrame(data[1:], columns=data[0])
    filename = f"central_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)

if __name__ == "__main__":
    scrape_central()
