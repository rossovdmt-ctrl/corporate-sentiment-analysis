class ToneAnalyzer:
    def __init__(self, tone_dict, preprocessor):
        self.tone_dict = tone_dict
        self.preprocessor = preprocessor
        self.min_words = 100

    def analyze(self, text):
        if not text or len(text) < 200:
            return None

        words = self.preprocessor.preprocess(text)
        if len(words) < self.min_words:
            return None

        pos = neg = known = 0
        for w in words:
            score = self.tone_dict.get_tone(w)
            if score != 0:
                known += 1
                if score > 0:
                    pos += 1
                elif score < 0:
                    neg += 1

        if known == 0:
            return None

        total = len(words)
        return {
            'pos_ratio': round(pos / total * 100, 2),
            'neg_ratio': round(neg / total * 100, 2),
            'known_ratio': round(known / total * 100, 2),
            'total_words': total
        }
