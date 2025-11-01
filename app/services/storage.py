import json
import os
from app.models import Article

class ArticleStorage:
    def __init__(self,storage_path):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path),exist_ok=True)
        if not os.path.exists(self.storage_path):
            self.write_articles([])
            print("Created new storage file !!")

    def read_articles(self) -> list[Article]:
        try:
            with open(self.storage_path,'r',encoding='utf-8') as f:
                data = json.load(f)

            articles = []
            for article_dict in data:
                article = Article(title=article_dict['title'],
                                  description=article_dict['description'],
                                  content=article_dict['content'],
                                  url=article_dict['url'],
                                  source_name=article_dict['source_name'],
                                  published_at=article_dict['published_at'],
                                  author=article_dict['author']
                                  )
                articles.append(article)

            return articles
        except Exception as e:
            print(f"Error reading articles from storage: {e}")
            return []

    def save_articles(self,articles :list[Article]):
        existing_articles = self._read_articles()
        exisiting_articles_ids = {article.id for article in existing_articles}

        count_new = 0
        count_duplicates = 0
        for article in articles:
            if article.id not in exisiting_articles_ids:
                existing_articles.append(article)
                count_new+=1
            else:
                count_duplicates+=1

        print(f"New Articles: {count_new}")
        print(f"Duplicate Articles: {count_duplicates}")

        self.write_articles(existing_articles)           
        return len(existing_articles)

    def write_articles(self,articles :list[Article]):
        try:
            with open(self.storage_path,'w',encoding='utf-8') as f:
                json.dump([article.to_dict() for article in articles],f)
            return len(articles)
        except Exception as e:
            print(f"Error writing articles to storage: {e}")

    def get_stats(self):
        articles = self.read_articles()
        print(f"Total Articles: {len(articles)}")
        return len(articles)

    def clear_storage(self):
        self.write_articles([])
        print("Storage cleared !!")
