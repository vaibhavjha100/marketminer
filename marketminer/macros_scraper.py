'''
Module for scraping macros data from various sources.
'''

import logging
import requests
import io
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_driver(download_dir="downloads"):
    # Make sure download folder exists
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Auto download Excel without popup
    prefs = {
        "download.default_directory": os.path.abspath(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_rbi_file(button_text: str, filename: str, download_dir="downloads"):
    driver = setup_driver(download_dir)

    try:
        driver.get("https://data.rbi.org.in/DBIE/#/dbie/home")

        wait = WebDriverWait(driver, 20)

        link = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(., '{button_text}')]"))
        )
        link.click()

        # Wait for download to complete
        time.sleep(15)  # adjust depending on network speed

        # Find latest downloaded file
        files = sorted(
            [os.path.join(download_dir, f) for f in os.listdir(download_dir)],
            key=os.path.getctime
        )
        downloaded_file = files[-1]

        # Rename to expected filename
        new_path = os.path.join(download_dir, filename)
        os.rename(downloaded_file, new_path)

        print(f"✅ Downloaded: {new_path}")
        return new_path

    finally:
        driver.quit()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by combining all the sheets and cleaning the data.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """


def scrape_macro_india(start_date: str = None, end_date: str = None)-> pd.DataFrame:
    """
    Scrape macroeconomic data for India from RBI website.

    Parameters:
    start_date (str, optional): Start date for the data in 'YYYY-MM-DD' format. Defaults to None.
    end_date (str, optional): End date for the data in 'YYYY-MM-DD' format. Defaults to None.
    Returns:
    pd.DataFrame: A DataFrame containing the macroeconomic data, indexed by date and sorted ascending.
    """

    logger.info(f"Scraping macroeconomic data from RBI")

    # Download both files
    f1 = download_rbi_file("50 Macroeconomic Indicators", "macroeconomic_indicators.xlsx")
    f2 = download_rbi_file("Other Macroeconomic Indicators", "other_macroeconomic_indicators.xlsx")

    # # Load into pandas
    # df1 = pd.read_excel(f1)
    # df2 = pd.read_excel(f2)
    #
    # # Clean and merge
    # merged_df = pd.concat([df1, df2], ignore_index=True)
    #
    # return merged_df
