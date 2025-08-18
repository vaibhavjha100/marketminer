from marketminer.fundamentals_scraper import scrape_fundamentals

if __name__ == "__main__":
    # Example ticker for Reliance Industries Limited
    ticker = 'ADANIENT'

    # Scrape the fundamentals data
    financial_data = scrape_fundamentals(ticker)

    # Display the scraped data
    print("Profit & Loss Data:")
    print(financial_data["profit_loss"].head())

    print("\nBalance Sheet Data:")
    print(financial_data["balance_sheet"].head())

    print("\nCash Flow Data:")
    print(financial_data["cash_flows"].head())

    print("\nRatios Data:")
    print(financial_data["ratios"].head())