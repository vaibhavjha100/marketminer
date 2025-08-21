from marketminer.macros_scraper import scrape_macro_india

if __name__ == "__main__":
    # Example usage of the scrape_macro_india function
    start_date = "2020-01-01"
    end_date = "2023-12-31"

    dic = scrape_macro_india(start_date=start_date, end_date=end_date)

    for sheet_name, data in dic.items():
        print(f"Sheet: {sheet_name}")
        print(data.head())
        print("\n")
        print(data.info())