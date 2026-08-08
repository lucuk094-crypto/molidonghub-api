import cloudscraper

scraper = cloudscraper.create_scraper()

urls_to_test = [
    "https://anichin.care",
    "https://anichin.care/anime",
    "https://anichin.care/donghua",
    "https://www.anichin.care",
    "https://anichin.club",
]

print("Testing URLs...")
print("=" * 60)

for url in urls_to_test:
    try:
        response = scraper.get(url, timeout=10)
        print(f"\n✓ {url}")
        print(f"  Status: {response.status_code}")
        print(f"  Final URL: {response.url}")
        if response.status_code == 200:
            # Check if page has content
            if len(response.text) > 1000:
                print(f"  Content: {len(response.text)} bytes (OK)")
            else:
                print(f"  Content: {len(response.text)} bytes (Too small?)")
    except Exception as e:
        print(f"\n✗ {url}")
        print(f"  Error: {str(e)[:100]}")

print("\n" + "=" * 60)
