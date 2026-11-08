import os
import re
import pickle
import subprocess
import sys

# Добавляем путь к src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DICT_PATH, RAW_REPORTS_DIR

def run():
    print("📖 Создание словаря EcSentiThemeLex...")
    
    # Устанавливаем библиотеку, если её нет
    try:
        from ecsentithemelex import Vocabulary
    except ImportError:
        print("Устанавливаем ecsentithemelex...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ecsentithemelex", "pymystem3", "-q"])
        from ecsentithemelex import Vocabulary

    word_tone_dict = {}
    
    # Проходим по всем словам в словаре
    for row in Vocabulary().all_word_tone_theme().itertuples():
        for w in str(row.Phrase).split():
            w = re.sub(r'[^\w\s]', '', w).lower().strip()
            if w:
                # Берем максимальную оценку, если слово встречается несколько раз
                word_tone_dict[w] = max(word_tone_dict.get(w, -999), row.Score)

    # Сохраняем в папку data/raw
    os.makedirs(RAW_REPORTS_DIR, exist_ok=True)
    with open(DICT_PATH, 'wb') as f:
        pickle.dump(word_tone_dict, f)
        
    print(f"✅ Словарь успешно создан и сохранен в {DICT_PATH}")
    print(f"   Всего слов: {len(word_tone_dict)}")

if __name__ == "__main__":
    run()
