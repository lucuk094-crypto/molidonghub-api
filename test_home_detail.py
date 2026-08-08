import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.utils.parsing import Parsing
from bs4 import BeautifulSoup

print("Testing Home Page Parsing...")
print("=" * 60)

parser = Parsing()
data = parser.get_parsed_html("/")

if data:
    print("✓ Successfully fetched and parsed HTML")
    
    # Check for bixbox sections
    bixboxes = data.find_all("div", {"class": "bixbox"})
    print(f"\nFound {len(bixboxes)} bixbox sections")
    
    # Check for articles
    articles = data.find_all("article")
    print(f"Found {len(articles)} articles total")
    
    if articles:
        print("\nFirst article structure:")
        first = articles[0]
        print(f"  Classes: {first.get('class')}")
        
        # Check for title
        title_div = first.find("div", {"class": "tt"})
        if title_div:
            print(f"  Has title div: ✓")
            h2 = title_div.find("h2")
            if h2:
                print(f"  Title (h2): {h2.text.strip()[:50]}")
        else:
            print(f"  Has title div: ✗")
            # Try alternative selectors
            alt_title = first.find("h2")
            if alt_title:
                print(f"  Alternative h2: {alt_title.text.strip()[:50]}")
        
        # Check for type
        type_div = first.find("div", {"class": "typez"})
        if type_div:
            print(f"  Has type div: ✓ ({type_div.text.strip()})")
        else:
            print(f"  Has type div: ✗")
        
        # Check for thumbnail
        img = first.find("img")
        if img:
            print(f"  Has img: ✓")
            print(f"    src: {img.get('src', '')[:50]}")
            print(f"    data-src: {img.get('data-src', '')[:50]}")
            print(f"    data-lazy-src: {img.get('data-lazy-src', '')[:50]}")
        else:
            print(f"  Has img: ✗")
        
        # Check for link
        link = first.find("a", href=True)
        if link:
            print(f"  Has link: ✓ ({link.get('href', '')[:50]})")
        else:
            print(f"  Has link: ✗")
            
else:
    print("✗ Failed to fetch HTML")

print("=" * 60)
