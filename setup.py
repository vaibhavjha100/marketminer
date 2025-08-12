from setuptools import setup, find_packages

setup(
    name="marketminer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas"
    ],
)
