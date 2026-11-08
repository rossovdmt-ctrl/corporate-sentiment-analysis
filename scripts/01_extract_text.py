import os
import sys
import pandas as pd
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import RAW_REPORTS_DIR, PROCESSED_DIR, DICT_PATH
from src.preprocessor import TextPreprocessor
from src.dictionary import ToneDictionary
from src.analyzer import ToneAnalyzer

def run():
    print("🚀 Запуск извлечения текста...")
    
    preprocessor = TextPreprocessor()
    tone_dict = ToneDictionary(DICT_PATH)
    analyzer = ToneAnalyzer(tone_dict, preprocessor)

    files = []
    for root, _, names in os.walk(RAW_REPORTS_DIR):
        for name in names:
            if name.lower().endswith(('.pdf', '.txt')):
                files.append(os.path.join(root, name))

    print(f"Найдено файлов: {len(files)}")
    results = []
    
    for file_path in tqdm(files):
        text = preprocessor.extract_text(file_path)
        if text:
            stats = analyzer.analyze(text)
            if stats:
                results.append(stats)

    if results:
        df = pd.DataFrame(results)
        df.to_csv(os.path.join(PROCESSED_DIR, 'df_all.csv'), index=False)
        print(f"✅ Готово! Сохранено {len(df)} записей.")

if __name__ == "__main__":
    run()
