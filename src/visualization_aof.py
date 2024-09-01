import matplotlib.pyplot as plt
import seaborn as sns

# (AOF) Frekans gösteren yatay bar grafiği
def create_frequency_bar_for_aof(df, total_students):
    # Çubuk grafiği
    plt.figure(figsize=(16, 14))
    ax = sns.barplot(x='f', y='PROGRAM', hue='DURUM', data=df, orient='h', dodge=True, width=0.9, ci=None)

    # Frekansları çubukların yanına doğru şekilde ekleme
    for p in ax.patches:
        width = int(p.get_width())
        position = (p.get_width(), p.get_y() + p.get_height() / 2)
        ax.annotate(f'{width}', xy=position, xytext=(5, 0), textcoords='offset points', ha='left', va='center', fontsize=6)

    # Yazı tipi boyutlarını ayarlama
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Frekans', fontsize=14)
    plt.ylabel('Program', fontsize=12)
    plt.title('Görme Engelli Öğrencilerin Programlar ve Öğrenim Durumlarına Göre Frekans Dağılımı', fontsize=16)

    # Toplam öğrenci sayısını hesaplama ve legend'de gösterme
    total_aktif = total_students.loc[total_students['DURUM'] == 'AKTİF', 'Toplam Öğrenci Sayısı'].values[0]
    total_pasif = total_students.loc[total_students['DURUM'] == 'PASİF', 'Toplam Öğrenci Sayısı'].values[0]

    # Legend'deki AKTİF ve PASİF etiketlerinin yanına toplam öğrenci sayısını ekleme
    handles, labels = ax.get_legend_handles_labels()
    new_labels = [f'AKTİF ({total_aktif})' if 'AKTİF' in label else f'PASİF ({total_pasif})' for label in labels]
    ax.legend(title='Öğrenim Durumu (f)', handles=handles, labels=new_labels, loc='lower right', fontsize=12, title_fontsize=14)

    plt.tight_layout()
    plt.show()
