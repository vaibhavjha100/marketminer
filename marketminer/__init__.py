'''
MarketMiner: A Python library for scraping financial data from various sources.
'''

__version__ = '0.6.0'

from .news_scraper import scrape_economic_times
from .fundamentals_scraper import scrape_fundamentals
from .macros_scraper import scrape_macro_india

__all__ = [
    'scrape_economic_times',
    'scrape_fundamentals',
    'scrape_macro_india',
]