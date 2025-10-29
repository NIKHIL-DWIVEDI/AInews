# debug_3_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"

print("Testing /fetch-news endpoint")
print("=" * 60)

# Test with minimal parameters
payload = {
    "country": "us",
    "page_size": 3
}

print(f"Payload: {payload}\n")

response = requests.post(f"{BASE_URL}/fetch-news", json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}\n")

if response.status_code == 200:
    articles = response.json()
    print(f"✅ Success! Got {len(articles)} articles")
    if articles:
        print(f"\nFirst article keys: {list(articles[0].keys())}")
        print(f"\nFirst article:")
        for key, value in articles[0].items():
            val_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"  {key}: {val_preview}")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response body: {response.text}")