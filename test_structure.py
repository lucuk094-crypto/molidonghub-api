import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

print("Analyzing anichin.care structure...")
print("=" * 60)

response = scraper.get("https://anichin.care", timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

# Check for main menu/navigation links
print("\n[NAVIGATION LINKS]")
nav_links = soup.find_all('a', href=True)
unique_paths = set()
for link in nav_links[:50]:  # Check first 50 links
    href = link.get('href', '')
    if href.startswith('/') and len(href) > 1:
        path = href.split('?')[0].split('#')[0]
        unique_paths.add(path)

for path in sorted(unique_paths):
    print(f"  {path}")

# Check for anime/donghua listings
print("\n[CONTENT SECTIONS]")
sections = soup.find_all(['div', 'section'], class_=True)
for section in sections[:20]:
    classes = ' '.join(section.get('class', []))
    if any(keyword in classes for keyword in ['anime', 'list', 'content', 'bixbox', 'releases']):
        print(f"  Found section: {classes[:50]}")

# Check for genre filters
print("\n[GENRE FILTERS]")
genre_inputs = soup.find_all('input', {'name': 'genre[]'})
if genre_inputs:
    print(f"  Found {len(genre_inputs)} genre inputs")
    for inp in genre_inputs[:5]:
        print(f"    - {inp.get('value')}")
else:
    print("  No genre inputs found")

# Check for articles (anime cards)
print("\n[ANIME CARDS]")
articles = soup.find_all('article')
print(f"  Found {len(articles)} articles on homepage")
if articles:
    first_article = articles[0]
    print(f"  First article classes: {first_article.get('class')}")
    title = first_article.find('h2')
    if title:
        print(f"  First title: {title.text.strip()[:50]}")

print("\n" + "=" * 60)
