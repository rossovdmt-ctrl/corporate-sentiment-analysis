import pandas as pd
import numpy as np

class ITFACalculator:
    """
    Модуль расчета Индекса текстово-финансовой аномалии (ИТФА).
    Реализует формулы (5)-(9) из статьи.
    """
    
    def __init__(self, data: pd.DataFrame, group_col: str = 'company_clean'):
        self.data = data
        self.group_col = group_col

    def calculate(self):
        results = []
        
        for company_group, group_data in self.data.groupby(self.group_col):
            data = group_data.sort_values('year').copy()

            # 1. Относительные изменения (Формулы 6 и 7)
            data['delta_pos'] = data['pos_ratio'].pct_change() * 100
            data['delta_profit_next'] = data['profit'].shift(-1).pct_change() * 100

            # Ограничение экстремальных выбросов прибыли (Winsorization)
            data['delta_profit_next_clipped'] = data['delta_profit_next'].clip(lower=-300.0, upper=300.0)

            # Убираем NaN
            valid_data = data.dropna(subset=['delta_pos', 'delta_profit_next_clipped'])
            N_c_L = len(valid_data)

            if N_c_L == 0:
                continue

            # 2. Индикатор аномалии (Формула 8)
            anomaly_mask = (valid_data['delta_pos'] > 0) & (valid_data['delta_profit_next_clipped'] < 0)
            anomaly_data = valid_data[anomaly_mask]

            # 3. Расчет ИТФА (Формула 9)
            if len(anomaly_data) > 0:
                itfa_score = (abs(anomaly_data['delta_pos']) + abs(anomaly_data['delta_profit_next_clipped'])).mean()
                mean_delta_pos = anomaly_data['delta_pos'].mean()
                mean_delta_profit = anomaly_data['delta_profit_next'].mean()
            else:
                itfa_score = 0.0
                mean_delta_pos = valid_data['delta_pos'].mean()
                mean_delta_profit = valid_data['delta_profit_next'].mean()

            results.append({
                'Компания (тип отчёта)': company_group,
                'ИТФА (п.п.)': round(itfa_score, 2),
                'N_c^L': N_c_L,
                'Средний δPos (аном.), %': round(mean_delta_pos, 2),
                'Средний δF (аном.), %': round(mean_delta_profit, 2)
            })

        df_itfa = pd.DataFrame(results).sort_values('ИТФА (п.п.)', ascending=False)
        
        # Динамический порог (верхний квартиль)
        non_zero_itfa = df_itfa[df_itfa['ИТФА (п.п.)'] > 0]['ИТФА (п.п.)']
        dynamic_threshold = non_zero_itfa.quantile(0.75) if len(non_zero_itfa) > 0 else 20.0
        
        return df_itfa, dynamic_threshold
