from envs.tf.Lib.ctypes import pythonapi
from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="marketminer",
    version="0.1.0",
    author="Vaibhav Jha",
    author_email="vaibhavjha100@gmail.com",
    description="A Python library for scraping financial data from various sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vaibhavjha100/marketminer.git",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas"
    ],
    python_requires=">=3.7"
)
