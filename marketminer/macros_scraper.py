'''
Module for scraping macros data from various sources.
'''

import logging
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

def setup_driver(download_dir="macro_downloads"):
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

def download_rbi_file(button_text: str, filename: str, download_dir="macro_downloads"):
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

def clean_data(main) -> dict:
    """
    Clean the DataFrame by combining all the sheets and cleaning the data.

    Parameters:
    main (bool): If True, clean like the main macro50 file.
                 If False, clean like the other macro file.

    Returns:
    dict: A dictionary with cleaned DataFrames for each sheet.
    """
    if main:
        file_path = 'macro_downloads/macroeconomic_indicators.xlsx'

        # Read the Excel file with all sheets
        df = pd.read_excel(
            file_path,
            sheet_name=None,
            engine='openpyxl',
            header=3
        )

        cleaned_data = {}
        for sheet_name, sheet_data in df.items():
            # Drop the 1st column from each sheet
            sheet_data = sheet_data.iloc[:, 1:]
            # Set the first column as index
            sheet_data.set_index(sheet_data.columns[0], inplace=True, drop=True)
            # Make the index a datetime index
            sheet_data.index = pd.to_datetime(sheet_data.index, errors='coerce')
            # Drop columns with Unnamed in the name
            sheet_data = sheet_data.loc[:, ~sheet_data.columns.str.contains('^Unnamed')]
            # Sort index
            sheet_data.sort_index(inplace=True)

            cleaned_data[sheet_name] = sheet_data
        return cleaned_data

    else:
        file_path = 'macro_downloads/other_macroeconomic_indicators.xlsx'

        # Read the Excel file with all sheets
        df = pd.read_excel(
            file_path,
            sheet_name=None,
            engine='openpyxl',
            header=1
        )

        cleaned_data = {}

        for sheet_name, sheet_data in df.items():
            # Drop the Unnamed: 0 column from each sheet
            sheet_data = sheet_data.iloc[:, 1:]
            # Drop the first 1 row
            sheet_data = sheet_data.drop(sheet_data.index[:1])
            # Set the first column as index
            sheet_data.set_index(sheet_data.columns[0], inplace=True, drop=True)
            # Make the index a datetime index
            sheet_data.index = pd.to_datetime(sheet_data.index, errors='coerce')
            # Drop columns with Unnamed in the name
            sheet_data = sheet_data.loc[:, ~sheet_data.columns.str.contains('^Unnamed')]
            # Sort index
            sheet_data.sort_index(inplace=True)

            cleaned_data[sheet_name] = sheet_data
        return cleaned_data



def scrape_macro_india(start_date: str = None, end_date: str = None)-> dict:
    """
    Scrape macroeconomic data for India from RBI website.

    Parameters:
    start_date (str, optional): Start date for the data in 'YYYY-MM-DD' format. Defaults to None.
    end_date (str, optional): End date for the data in 'YYYY-MM-DD' format. Defaults to None.
    Returns:
    dict: A dictionary containing cleaned DataFrames for each sheet.
    """

    logger.info(f"Scraping macroeconomic data from RBI")

    # Download both files
    download_rbi_file("50 Macroeconomic Indicators", "macroeconomic_indicators.xlsx")
    download_rbi_file("Other Macroeconomic Indicators", "other_macroeconomic_indicators.xlsx")

    # Clean the data
    d1 = clean_data(main=True)
    d2 = clean_data(main=False)

    # Merge the two dictionaries key-wise
    # Weekly data will be merged with weekly data, monthly with monthly, etc.
    merged = {}
    for key in d1.keys():
        if key in d2:
            merged[key] = pd.concat([d1[key], d2[key]], axis=0)
        else:
            merged[key] = d1[key]

    for key in d2.keys():
        if key not in merged:
            merged[key] = d2[key]

    # Filter data based on start_date and end_date
    start_date = pd.to_datetime(start_date) if start_date else None
    end_date = pd.to_datetime(end_date) if end_date else None

    for key in merged.keys():
        if start_date:
            merged[key] = merged[key][merged[key].index >= start_date]
        if end_date:
            merged[key] = merged[key][merged[key].index <= end_date]

    # Delete the whole macro_downloads folder
    download_dir = "macro_downloads"
    if os.path.exists(download_dir):
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                logger.error(f"Failed to delete {file_path}. Reason: {e}")
        os.rmdir(download_dir)
            
    logger.info("Scraping completed for macroeconomic data successfully.")

    return merged
