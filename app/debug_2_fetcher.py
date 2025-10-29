# debug_2_fetcher.py
from services.news_fetcher import NewsFetcher
from models import Article

print("=" * 60)
print("Testing NewsFetcher Class")
print("=" * 60)

fetcher = NewsFetcher()

# Test 1: Basic fetch
print("\nTest 1: Basic fetch (no category)")
print("-" * 60)

try:
    articles = fetcher.fetch_news(country="us", page_size=3)
    print(f"✅ Returned: {len(articles)} articles")
    print(f"   Type: {type(articles)}")
    
    if articles:
        article = articles[0]
        print(f"\nFirst article:")
        print(f"  Type: {type(article)}")
        print(f"  Title: {article.title}")
        print(f"  ID: {article.id}")
        print(f"\n  to_dict() keys: {list(article.to_dict().keys())}")
        print(f"\n  to_dict() values:")
        for key, value in article.to_dict().items():
            val_preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"    {key}: {val_preview}")
    else:
        print("⚠️  Empty list returned")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

# Test 2: With category
print("\n" + "=" * 60)
print("Test 2: With category (technology)")
print("-" * 60)

try:
    articles = fetcher.fetch_news(country="us", category="technology", page_size=3)
    print(f"✅ Returned: {len(articles)} articles")
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article.title[:50]}...")
    else:
        print("⚠️  Empty list returned")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check parse_articles
print("\n" + "=" * 60)
print("Test 3: Test parse_articles directly")
print("-" * 60)

sample_raw_article = {
    "title": "Test Article",
    "description": "Test description",
    "content": "Test content",
    "url": "https://example.com",
    "source": {"name": "Test Source"},
    "publishedAt": "2025-10-29T00:00:00Z",
    "author": "Test Author"
}

try:
    parsed = fetcher.parse_articles([sample_raw_article])
    print(f"✅ Parsed: {len(parsed)} articles")
    if parsed:
        print(f"   Article object created successfully")
        print(f"   Keys in to_dict(): {list(parsed[0].to_dict().keys())}")
except Exception as e:
    print(f"❌ Parse failed: {e}")
    import traceback
    traceback.print_exc()