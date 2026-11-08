import os
import pickle

class ToneDictionary:
    def __init__(self, dict_path):
        self.dict_path = dict_path
        self.word_tone_dict = {}
        self.load_or_create()

    def load_or_create(self):
        if os.path.exists(self.dict_path):
            with open(self.dict_path, 'rb') as f:
                self.word_tone_dict = pickle.load(f)
        else:
            print("Словарь не найден. Запустите скрипт создания словаря.")

    def get_tone(self, word):
        return self.word_tone_dict.get(word, 0)
