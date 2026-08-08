import cloudscraper

scraper = cloudscraper.create_scraper()

print("Testing anichin.moe...")
print("=" * 60)

try:
    response = scraper.get("https://anichin.moe", timeout=15)
    print(f"Status: {response.status_code}")
    print(f"Final URL: {response.url}")
    print(f"Content length: {len(response.text)} bytes")
    print(f"\nFirst 1500 chars:")
    print(response.text[:1500])
    print("\n...")
    print(f"\nHas <article>: {'<article' in response.text}")
except Exception as e:
    print(f"Error: {e}")

print("=" * 60)
