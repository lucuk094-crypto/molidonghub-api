import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cloudscraper

scraper = cloudscraper.create_scraper()
response = scraper.get("https://anichin.moe", timeout=15)

print(f"Status: {response.status_code}")
print(f"Encoding: {response.encoding}")
print(f"Content length: {len(response.text)} bytes")

# Save HTML
with open("anichin_homepage.html", "w", encoding="utf-8") as f:
    f.write(response.text)
    
print("✓ HTML saved to anichin_homepage.html")

# Check structure
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article')
print(f"\nArticles found: {len(articles)}")

# Check various class names
for class_name in ['bixbox', 'listupd', 'bs', 'bsx', 'card']:
    elements = soup.find_all(class_=class_name)
    if elements:
        print(f"Elements with class '{class_name}': {len(elements)}")
