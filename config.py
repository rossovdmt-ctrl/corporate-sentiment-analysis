import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_REPORTS_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
PLOTS_DIR = os.path.join(BASE_DIR, "output", "plots")

for path in [PROCESSED_DIR, PLOTS_DIR, RAW_REPORTS_DIR]:
    os.makedirs(path, exist_ok=True)

MIN_REPORTS_THRESHOLD = 7
DICT_PATH = os.path.join(RAW_REPORTS_DIR, "word_tone_dict.pkl")
FINANCE_EXCEL_PATH = os.path.join(RAW_REPORTS_DIR, "Прибыль.xlsx")
