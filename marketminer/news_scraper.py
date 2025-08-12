'''
Module for scraping news articles from various sources.
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import logging
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/120.0.0.0 Safari/537.36"
}

CATEGORIES = [
    "https://economictimes.indiatimes.com/news/company",
    "https://economictimes.indiatimes.com/news/economy",
    "https://economictimes.indiatimes.com/markets",
    "https://economictimes.indiatimes.com/industry"
]

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
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")

    for category_url in CATEGORIES:
        logger.info(f"Scraping category: {category_url}")
        for page in range(1,5):
            url = f"{category_url}/{page}" if page > 1 else category_url
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                logger.error(f"Failed to fetch {url}")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.select("div.eachStory")

            if not articles:
                logger.info(f"No articles found on {url}")
                break

            for article in articles:
                headline_tag = article.find("h3")
                link_tag = article.find("a")
                date_tag = article.find("time") or article.find("span", class_="date")
                body = article.find("p")

                if not (headline_tag and link_tag and date_tag):
                    continue

                headline = headline_tag.text.strip()
                link = link_tag.get("href")
                if link and not link.startswith("http"):
                    link = "https://economictimes.indiatimes.com" + link

                body = body.text.strip() if body else ""

                try:
                    pub_date = datetime.strptime(date_tag.text.strip(), "%b %d, %Y")
                except ValueError:
                    continue

                if start_dt <= pub_date <= end_dt:
                    results.append({
                        "headline": headline,
                        "link": link,
                        "category": category_url.split("/")[-1],
                        "date": pub_date.strftime("%d/%m/%Y"),
                        "body": body
                    })
                elif pub_date < start_dt:
                    # Stop scraping older articles
                    break

    # Make the results unique by headline and link
    df = pd.DataFrame(results)
    df.drop_duplicates(subset=["headline", "link"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    if df.empty:
        logger.info("No articles found in the specified date range.")
        return pd.DataFrame(columns=["headline", "link", "category", "date", "body"])

    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    logger.info(f"Scraped {len(df)} articles from Economic Times.")

    return df