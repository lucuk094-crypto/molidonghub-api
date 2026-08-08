import sys
sys.path.insert(0, '.')

from api.utils.parsing import Parsing
from bs4 import BeautifulSoup

parser = Parsing()
data = parser.get_parsed_html("/")

if data:
    print("✓ HTML fetched and parsed")
    
    # Check for bixbox
    bixboxes = data.find_all("div", class_="bixbox")
    print(f"\nTotal bixbox divs: {len(bixboxes)}")
    
    if bixboxes:
        print("\nFirst bixbox:")
        first_box = bixboxes[0]
        
        # Check for header
        headers = first_box.find_all(["h1", "h2", "h3"])
        if headers:
            print(f"  Headers found: {[h.text.strip()[:50] for h in headers]}")
        
        # Check for articles
        articles = first_box.find_all("article", class_="bs")
        print(f"  Articles with class 'bs': {len(articles)}")
        
        if articles:
            first_article = articles[0]
            bsx = first_article.find("div", class_="bsx")
            if bsx:
                print("  First article has bsx div: ✓")
                link = bsx.find("a", href=True)
                if link:
                    print(f"    Link: {link.get('href')[:50]}")
                tt = bsx.find("div", class_="tt")
                if tt:
                    h2 = tt.find("h2")
                    if h2:
                        print(f"    Title: {h2.text.strip()[:50]}")
    else:
        print("\n✗ No bixbox divs found!")
        print("\nSearching for any divs with 'box' in class name:")
        all_divs = data.find_all("div", class_=True)
        box_divs = [d for d in all_divs if any('box' in c.lower() for c in d.get('class', []))]
        print(f"Found {len(box_divs)} divs with 'box' in class")
        if box_divs:
            for div in box_divs[:5]:
                print(f"  - {div.get('class')}")
else:
    print("✗ Failed to fetch HTML")
