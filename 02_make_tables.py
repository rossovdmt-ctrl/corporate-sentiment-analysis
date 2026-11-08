import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import PROCESSED_DIR, MIN_REPORTS_THRESHOLD
from src.statistics import MetricsCalculator

def run():
    df_all = pd.read_csv(os.path.join(PROCESSED_DIR, 'df_all.csv'))
    
    counts = df_all.groupby('company_clean').size()
    reliable = counts[counts >= MIN_REPORTS_THRESHOLD].index
    df = df_all[df_all['company_clean'].isin(reliable)].copy()
    df.to_csv(os.path.join(PROCESSED_DIR, 'df_filtered.csv'), index=False)

    sync_results = []
    lag_results = []
    conc_sync = []
    conc_lag = []
    
    for company, group in df.groupby('company_clean'):
        if len(group) < 5: continue
        
        r_pos, _ = MetricsCalculator.calc_pearson(group, 'pos_ratio', 'profit', lag=False)
        r_neg, _ = MetricsCalculator.calc_pearson(group, 'neg_ratio', 'profit', lag=False)
        if r_pos is not None:
            sync_results.append({'Компания': company, 'Поз→Приб (r)': r_pos, 'Нег→Приб (r)': r_neg})
            
        r_pos_lag, _ = MetricsCalculator.calc_pearson(group, 'pos_ratio', 'profit', lag=True)
        r_neg_lag, _ = MetricsCalculator.calc_pearson(group, 'neg_ratio', 'profit', lag=True)
        if r_pos_lag is not None:
            lag_results.append({'Компания': company, 'Поз→Приб (r)': r_pos_lag, 'Нег→Приб (r)': r_neg_lag})

        direct_pos, _ = MetricsCalculator.calc_concordance(group, 'pos_ratio', 'profit', lag=False)
        direct_neg, _ = MetricsCalculator.calc_concordance(group, 'neg_ratio', 'profit', lag=False)
        if direct_pos is not None:
            conc_sync.append({'Компания': company, 'Поз(↑↑/↓↓)': direct_pos, 'Нег(↑↑/↓↓)': direct_neg})
            
        direct_pos_l, _ = MetricsCalculator.calc_concordance(group, 'pos_ratio', 'profit', lag=True)
        direct_neg_l, _ = MetricsCalculator.calc_concordance(group, 'neg_ratio', 'profit', lag=True)
        if direct_pos_l is not None:
            conc_lag.append({'Компания': company, 'Поз(↑↑/↓↓)': direct_pos_l, 'Нег(↑↑/↓↓)': direct_neg_l})

    pd.DataFrame(sync_results).sort_values('Поз→Приб (r)', ascending=False).to_csv(os.path.join(PROCESSED_DIR, 'table2.csv'), index=False)
    pd.DataFrame(lag_results).sort_values('Поз→Приб (r)', ascending=False).to_csv(os.path.join(PROCESSED_DIR, 'table3.csv'), index=False)
    pd.DataFrame(conc_sync).sort_values('Поз(↑↑/↓↓)', ascending=False).to_csv(os.path.join(PROCESSED_DIR, 'table4.csv'), index=False)
    pd.DataFrame(conc_lag).sort_values('Поз(↑↑/↓↓)', ascending=False).to_csv(os.path.join(PROCESSED_DIR, 'table5.csv'), index=False)
    
    print("✅ Все таблицы (2-5) успешно сгенерированы!")

if __name__ == "__main__":
    run()
