import os
import re
import fitz
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

class TextPreprocessor:
    def __init__(self):
        self.stopwords = set(stopwords.words('russian'))

    def tokenize(self, text):
        if not text:
            return []
        return re.findall(r'[а-яёa-z]+', text.lower())

    def remove_stopwords(self, words):
        return [w for w in words if w not in self.stopwords]

    def preprocess(self, text):
        words = self.tokenize(text)
        return self.remove_stopwords(words)

    @staticmethod
    def extract_text(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            try:
                doc = fitz.open(file_path)
                text = ' '.join([p.get_text() for p in doc])
                doc.close()
                return text if len(text.strip()) >= 200 else None
            except Exception:
                return None
        elif ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return None
        return None
