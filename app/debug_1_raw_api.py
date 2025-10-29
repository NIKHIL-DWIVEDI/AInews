# debug_1_raw_api.py
import requests
import os
from dotenv import load_dotenv

from config import Config

load_dotenv()

# api_key = os.getenv("NEWS_API_KEY")
# print(f"API Key (first 10 chars): {api_key[:10]}...\n")
api_key = Config().news_api_key

# Test 1: Simplest possible request
print("=" * 60)
print("TEST 1: Absolute simplest request (top headlines, US)")
print("=" * 60)

url = "https://newsapi.org/v2/top-headlines"
params = {
    "apiKey": api_key,
    "country": "us",
    "pageSize": 3
}

print(f"URL: {url}")
print(f"Params: {params}\n")

response = requests.get(url, params=params)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}\n")

data = response.json()
print(f"Response JSON:")
print(f"  - status: {data.get('status')}")
print(f"  - totalResults: {data.get('totalResults')}")
print(f"  - articles count: {len(data.get('articles', []))}")

if data.get('status') == 'error':
    print(f"\n❌ API ERROR: {data.get('message')}")
    print(f"   Code: {data.get('code')}")
else:
    print(f"\n✅ API returned successfully")
    articles = data.get('articles', [])
    if articles:
        print(f"\nFirst article:")
        print(f"  Title: {articles[0].get('title')}")
        print(f"  Source: {articles[0].get('source', {}).get('name')}")
    else:
        print("\n⚠️  No articles in response")

# Test 2: With category
print("\n" + "=" * 60)
print("TEST 2: With category (technology)")
print("=" * 60)

params = {
    "apiKey": api_key,
    "country": "us",
    "category": "technology",
    "pageSize": 3
}

response = requests.get(url, params=params)
data = response.json()

print(f"Status Code: {response.status_code}")
print(f"Response status: {data.get('status')}")
print(f"Total results: {data.get('totalResults')}")
print(f"Articles count: {len(data.get('articles', []))}")

if data.get('status') == 'error':
    print(f"\n❌ ERROR: {data.get('message')}")

# Test 3: Check your API quota/account
print("\n" + "=" * 60)
print("IMPORTANT: Check your account")
print("=" * 60)
print("Go to: https://newsapi.org/account")
print("Check:")
print("  1. Requests used today")
print("  2. Requests remaining")
print("  3. Account status (active/suspended)")