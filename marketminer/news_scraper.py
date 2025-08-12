'''
Module for scraping news articles from various sources.
'''

import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
from datetime import datetime, timedelta, date
from .utils import date_to_excel_serial
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/120.0.0.0 Safari/537.36"
}

VALID_SECTIONS = ["company", "economy", "markets", "industry"]

def scrape_economic_times(start_date, end_date):
    """
    Scrape news articles from Economic Times within a date range.

    Parameters:
    start_date (str): Start date in the format 'YYYY-MM-DD'.
    end_date (str): End date in the format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame containing news articles.
    """
    results = []
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    curr_date = start_dt
    while curr_date <= end_dt:
        logger.info(f"Scraping archive for {curr_date.date()}...")
        year = int(curr_date.year)
        month = int(curr_date.month)
        starttime = date_to_excel_serial(curr_date.date())

        archive_url = f"https://economictimes.indiatimes.com/archivelist/year-{year},month-{month},starttime-{starttime}.cms"
        r = requests.get(archive_url, headers=HEADERS)
        if r.status_code != 200:
            logger.warning(f"Failed to fetch archive for {curr_date.date()}")
            curr_date += timedelta(days=1)
            continue

        soup = BeautifulSoup(r.content, "html.parser")
        count = 0
        for article in soup.select("a[href*='/industry/'], a[href*='/markets/'], a[href*='/wealth/'], a[href*='/small-biz/'], a[href*='/tech/']"):
            count += 1
            headline = article.text.strip()
            link = article['href']
            if count <4 or 'live' in link or 'articleshow' not in link:
                # Skip the first 3 articles which contain market data
                continue
            # Access link to get the full article body and more details
            r = requests.get(link, headers=HEADERS)
            article_soup = BeautifulSoup(r.content, "html.parser")
            match = re.search(r'/(?:amp_)?articleshow/(\d+)\.cms', link)
            article_id = match.group(1) if match else None
            body = ' '.join([p.get_text() for p in soup.select('.artText, .Normal')])

            results.append({
                "article_id": article_id,
                "headline": headline,
                "link": link,
                "date": curr_date.strftime("%Y-%m-%d"),
                "body": body
            })
        logger.info(f"Found {count} articles for {curr_date.date()}.")
        curr_date += timedelta(days=1)

    # Make the results unique by headline and link
    df = pd.DataFrame(results)
    df.drop_duplicates(subset=["headline", "link"], inplace=True)
    if df.empty:
        logger.info("No articles found in the specified date range.")
        return pd.DataFrame(columns=["headline", "link", "category", "date", "body"])

    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    logger.info(f"Scraped {len(df)} articles from Economic Times.")

    return df