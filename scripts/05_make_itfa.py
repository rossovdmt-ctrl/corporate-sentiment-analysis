import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import PROCESSED_DIR, PLOTS_DIR
from src.itfa_calculator import ITFACalculator
import matplotlib.pyplot as plt

def run():
    print("🚨 Расчет ИТФА (Индекс текстово-финансовой аномалии)...")
    
    # Загружаем данные
    df = pd.read_csv(os.path.join(PROCESSED_DIR, 'df_filtered.csv'))
    
    # Инициализируем калькулятор и считаем
    calculator = ITFACalculator(df)
    df_itfa, threshold = calculator.calculate()
    
    # Выводим результат
    print("\n" + "="*110)
    print("🚨 ТАБЛИЦА: Значения ИТФА по группам «компания — тип отчёта»")
    print("="*110)
    print(df_itfa.to_string(index=False))
    print("="*110)
    print(f"✅ Динамический порог (верхний квартиль): {threshold:.2f} п.п.")
    
    # Сохраняем таблицу
    df_itfa.to_csv(os.path.join(PROCESSED_DIR, 'table6_itfa.csv'), index=False)
    print(f"✅ Таблица сохранена: table6_itfa.csv")

    # --- СТРОИМ ГРАФИК ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['figure.dpi'] = 300

    df_plot = df_itfa.sort_values('ИТФА (п.п.)', ascending=True).copy()
    fig, ax = plt.subplots(figsize=(12, 10))

    colors = ['#C62828' if x >= threshold else '#FBC02D' for x in df_plot['ИТФА (п.п.)']]
    bars = ax.barh(df_plot['Компания (тип отчёта)'], df_plot['ИТФА (п.п.)'],
                   color=colors, alpha=0.85, edgecolor='black', linewidth=0.5)

    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(width + 1.5, bar.get_y() + bar.get_height()/2,
                    f'{width:.2f}', va='center', fontsize=10, fontweight='bold')

    ax.axvline(x=threshold, color='red', linestyle='--', linewidth=1.5,
               label=f'Порог аномальности ({threshold:.0f} п.п.)')

    ax.set_xlabel('Индекс текстово-финансовой аномалии (ИТФА), п.п.', fontsize=12)
    ax.set_title('Рейтинг групп «компания — тип отчёта» по риску манипуляции', fontsize=14, weight='bold')
    ax.legend(loc='lower right', fontsize=11)
    ax.set_xlim(0, max(df_plot['ИТФА (п.п.)']) * 1.15)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, '05_itfa_ranking.png'), dpi=300, bbox_inches='tight')
    print(f"✅ График сохранен: 05_itfa_ranking.png")
    plt.close()

if __name__ == "__main__":
    run()
