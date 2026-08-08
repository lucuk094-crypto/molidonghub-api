import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.utils.genre import Genres
from api.utils.home import Home

print("=" * 50)
print("Testing Anichin API Scraper")
print("=" * 50)

# Test 1: List Genres
print("\n[TEST 1] Fetching genres list...")
genres = Genres()
result = genres.list_genre()
print(f"Total genres found: {result.get('total', 0)}")
if result.get('genres'):
    print(f"First 5 genres: {result['genres'][:5]}")
else:
    print(f"ERROR: {result.get('error', 'No data')}")

# Test 2: Home page
print("\n[TEST 2] Fetching home page...")
home = Home(1)
result = home.get_details()
print(f"Total sections: {result.get('total', 0)}")
if result.get('results'):
    for section in result['results']:
        print(f"  - Section: {section['section']}, Items: {len(section['cards'])}")
else:
    print(f"ERROR: {result.get('error', 'No data')}")

print("\n" + "=" * 50)
print("Test completed!")
print("=" * 50)
