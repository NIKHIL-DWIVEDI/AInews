# debug_4_direct_call.py
from services.news_fetcher import NewsFetcher

fetcher = NewsFetcher()

print("Simulating FastAPI endpoint call")
print("=" * 60)

# This is what your FastAPI endpoint is doing
print("\nCall 1: Exactly as FastAPI calls it")
print("-" * 60)

# Simulate FetchNewsRequest with defaults
request_params = {
    "query": None,        # From Field(None)
    "country": "us",      # From Field("us")
    "category": None,     # From Field(None)
    "page_size": 3,
    "page": 1
}

print(f"Parameters: {request_params}\n")

try:
    articles = fetcher.fetch_news(
        query=request_params["query"],
        country=request_params["country"],
        category=request_params["category"],
        page_size=request_params["page_size"],
        page=request_params["page"]
    )
    print(f"✅ Result: {len(articles)} articles")
    
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

# Check what happens with None vs not passing the parameter
print("\n" + "=" * 60)
print("Call 2: Without explicitly passing None values")
print("-" * 60)

try:
    articles = fetcher.fetch_news(
        country="us",
        page_size=3
    )
    print(f"✅ Result: {len(articles)} articles")
    
except Exception as e:
    print(f"❌ Exception: {e}")