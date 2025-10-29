import hashlib

class Article:
    def __init__(self, title, description, content, url,source_name, published_at,author=None):
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.source_name = source_name
        self.published_at = published_at
        self.author = author
        self.id = self._generate_id()

    def _generate_id(self):
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()[:6]  ## use hashilib instead of hash for consistent hashing
    
    def get_full_text(self):
        parts = [
            f"Title: {self.title}",
            f"Description: {self.description}",
            f"Content: {self.content}",
            f"URL: {self.url}",
            f"Source: {self.source_name}",
            f"Published At: {self.published_at}",
            f"Author: {self.author}"
        ]
        return "\n".join(parts).strip() 
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "url": self.url,
            "source_name": self.source_name,
            "published_at": self.published_at,
            "author": self.author
        }
    
