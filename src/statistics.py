import numpy as np
from scipy.stats import pearsonr

class MetricsCalculator:
    @staticmethod
    def calc_pearson(data, metric_col, profit_col, lag=False):
        df = data.sort_values('year').copy()
        delta_t = df[metric_col].pct_change() * 100
        
        if lag:
            profit_next = df[profit_col].shift(-1)
            delta_f = profit_next.pct_change() * 100
        else:
            delta_f = df[profit_col].pct_change() * 100
            
        df_calc = df.assign(delta_t=delta_t, delta_f=delta_f).dropna(subset=['delta_t', 'delta_f'])
        
        if len(df_calc) < 4:
            return None, None
            
        r, p_value = pearsonr(df_calc['delta_t'], df_calc['delta_f'])
        return round(r, 3), round(p_value, 3)

    @staticmethod
    def calc_concordance(data, metric_col, profit_col, lag=False):
        df = data.sort_values('year').copy()
        delta_t = df[metric_col].pct_change() * 100
        
        if lag:
            profit_next = df[profit_col].shift(-1)
            delta_f = profit_next.pct_change() * 100
        else:
            delta_f = df[profit_col].pct_change() * 100
            
        sign_t = np.sign(delta_t)
        sign_f = np.sign(delta_f)
        
        mask = (sign_t != 0) & (sign_f != 0) & (~sign_t.isna()) & (~sign_f.isna())
        
        if mask.sum() < 4:
            return None, None
            
        matches = (sign_t[mask] == sign_f[mask])
        direct = matches.sum() / len(matches)
        inverse = 1 - direct
        
        return round(direct, 3), round(inverse, 3)
