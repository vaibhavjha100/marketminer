from marketminer.fundamentals_scraper import scrape_fundamentals
import pandas as pd

if __name__ == "__main__":
    # Example ticker for Reliance Industries Limited
    ticker = 'ADANIENT'

    # Scrape the fundamentals data
    financial_data = scrape_fundamentals(ticker)

    # Display the scraped data
    print("Profit & Loss Data:")
    print(financial_data[0].head())

    print("\nBalance Sheet Data:")
    print(financial_data[1].head())

    print("\nCash Flow Data:")
    print(financial_data[2].head())

    print("\nRatios Data:")
    print(financial_data[3].head())