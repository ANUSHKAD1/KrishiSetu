import schedule
import time
from scraper_central import scrape_central
from scraper_karnataka import scrape_karnataka

def job():
    scrape_central()
    scrape_karnataka()

schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
