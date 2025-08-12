from marketminer.news_scraper import scrape_economic_times
from datetime import datetime, timedelta

if __name__ == "__main__":
    # Choose a small date range to limit results
    df = scrape_economic_times('2025-01-01', '2025-01-02')
    print(df.head())
    print(df.info())