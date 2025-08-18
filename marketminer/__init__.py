'''
MarketMiner: A Python library for scraping financial data from various sources.
'''

__version__ = '0.5.0'

from .news_scraper import scrape_economic_times
from .fundamentals_scraper import scrape_fundamentals

__all__ = [
    'scrape_economic_times',
    'scrape_fundamentals',
]