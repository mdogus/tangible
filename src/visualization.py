import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Kategorik Dağılım
def plot_categorical_distribution(df, column_name, hue=None, title="Categorical Distribution", save_path=None, column_order=None, hue_order=None):
    # Bar sayısını hesapla
    bar_count = df[column_name].nunique()
    
    # fig_y değerini bar sayısına göre ayarlama
    fig_y = 3 if bar_count < 5 else 6 if 5 <= bar_count < 15 else 9 if 15 <= bar_count < 30 else 12
    # font_annotation değerini barsayısına göre ayarlama
    if hue:
        font_annotation = 11 if bar_count < 5 else 10 if 5 <= bar_count < 15 else 9 if 15 <= bar_count < 30 else 8 if 15 <= bar_count < 30 else 6 if 30 <= bar_count < 60 else 5
    else:
        font_annotation = 11 if bar_count < 5 else 10 if 5 <= bar_count < 15 else 9 if 15 <= bar_count < 30 else 8 if 15 <= bar_count < 30 else 6
    # box_style değerini bar sayısına göre ayarlama
    box_style = 'round,pad=0.3' if bar_count < 5 else 'round,pad=0.3' if 5 <= bar_count < 15 else 'round,pad=0.2' if 15 <= bar_count < 30 else 'round,pad=0.1' if 15 <= bar_count < 30 else 'round,pad=0'
    # xy_text pozisyonunu ayarlama
    xy_text = [5, 0] if bar_count < 5 else [3, 0]# if 5 <= bar_count < 15 else [0, 0] if 15 <= bar_count < 30 else [-3, 0] if 30 <= bar_count < 60 else [-3, 0]
    # palette değerini bar sayısına göre ayarlama
    palette = "Set1" if bar_count < 5 else 'Set2' if 5 <= bar_count < 15 else 'coolwarm' if 15 <= bar_count < 30 else 'Set2' if 30 <= bar_count < 45 else 'husl'
    #palette = "Set2"  # 'Set1', 'coolwarm', 'viridis'
    
    # Sütundaki kategorileri sıralama
    order = df[column_name].value_counts(ascending=True).index if column_order == "ascending" else df[column_name].value_counts(ascending=False).index if column_order == "descending" else None
    
    # Hue'daki kategorileri sıralama
    if hue:
        hue_order = df[hue].value_counts(ascending=True).index if hue_order == "ascending" else df[hue].value_counts(ascending=False).index if hue_order == "descending" else None
    else:
        hue_order = None
    
    # Dinamik olarak ayarlanmış figsize ile grafiği oluştur
    plt.figure(figsize=(10, fig_y))
    ax = sns.countplot(data=df, y=column_name, hue=hue, palette=palette, order=order, hue_order=hue_order)
    plt.title(title)
    plt.xlabel("Frekans")
    plt.ylabel(column_name)
    plt.xticks(rotation=0)

    # Frekansları çubukların yanına doğru şekilde ekleme
    for p in ax.patches:
        width = int(p.get_width())
        position = (p.get_width(), p.get_y() + p.get_height() / 2)
        ax.annotate(f'{width}', xy=position, 
                    xytext=(xy_text), textcoords='offset points', ha='left', va='center', 
                    color='black',
                    bbox=dict(facecolor='white', edgecolor='none', boxstyle=box_style), 
                    fontsize=font_annotation)

    if save_path:
        plt.savefig(save_path)
    
    plt.show()

# Pie chart
def plot_pie_chart(df, column_name, title="Pie Chart", explode=None, explode_index=None, labels_with_count=None, shadow=None, label_text=None, autopct_text=None, wedge_width=None):
    # Sütundaki farklı değişken sayısı
    var_count = df[column_name].nunique()
    # Verileri gruplandırma ve toplamlarını hesaplama
    data_counts = df[column_name].value_counts()
    
    colors = plt.get_cmap('Set2').colors

    # Explode parametresini oluşturma
    if explode_index:
        explode = [0] * len(data_counts)
        explode[explode_index] = 0.1 if explode_index is not None and explode_index < len(explode) else 0
    elif explode == True and var_count > 2:
        explode = [0.1 if i == data_counts.max() else 0 for i in data_counts]
    else:
        explode = [0] * len(data_counts)
    
    # Etiket formatlarını özelleştirme
    labels = [f'{label}\n({count})' for label, count in zip(data_counts.index, data_counts)] if labels_with_count == True else data_counts.index
    """
    # Yüzde etiketi
    def autopct_format(pct, total_count):
        absolute = int(round(pct * total_count / 100))
        return f"{absolute}\n(%{pct:.1f})"
    """
    # Pasta grafiği çizimi
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(data_counts, labels=labels, 
            #autopct=lambda pct: autopct_format(pct, data_counts.sum()), # autopct_format fonksiyonu
            autopct=lambda pct: f'%{pct:.1f}',
            wedgeprops=dict(width=0.4) if wedge_width else None,
            explode=explode, colors=colors, 
            shadow=shadow)
    
    # Etiketlerin arka plan rengini değiştirme
    if label_text:
        for text in texts:
            text.set_bbox(dict(facecolor='yellow', edgecolor='black', boxstyle='round,pad=0.3'))
    # Yüzdelik etiketler için arka plan rengini değiştirme
    if autopct_text:
        for autotext, color in zip(autotexts, colors):
            autotext.set_bbox(dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.3', linewidth=2, alpha=0.6))
    
    plt.title(title, fontdict={'weight':'bold'})
    plt.show()


def plot_numerical_distribution(df, column_name, title="Numerical Distribution"):
    plt.figure(figsize=(10,6))
    sns.histplot(df[column_name], kde=True)
    plt.title(title)
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.show()

def plot_crosstab(df, col1, col2, title="Cross Tabulation"):
    color_map = random.choice(['Set2', 'viridis', 'plasma', 'inferno', 'magma', 'Blues', 'Greens', 'Set1', 'Pastel1'])
    print('color_map: ' + color_map)

    plt.figure(figsize=(10,6))
    cross_tab = pd.crosstab(df[col1], df[col2])
    cross_tab.plot(kind='bar', stacked=True, colormap=color_map)
    plt.title(title)
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.xticks(rotation=45)
    plt.show()

def plot_scatter(df, col1, col2, title="Scatter Plot"):
    #plt.figure(figsize=(10,6))
    plt.scatter(df[col1], df[col2])
    plt.title(title)
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.show()

def plot_frequency_bar(frequency_df, col1, hue=None):
    #plt.figure(figsize=(12, 8))
    sns.barplot(data=frequency_df, x=col1, y='f', hue=hue)
    plt.title('Sıklık Analizi')
    plt.xlabel('Document')
    plt.ylabel('Frekans (f)')
    plt.xticks(rotation=45)
    plt.legend(title='Subtheme')
    plt.show()

def plot_frequency_heatmap(pivot_table):
    #plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt="d", cmap="YlGnBu")
    plt.title('Sıklık Analizi (Heatmap)')
    plt.xlabel('Subtheme')
    plt.ylabel('Document')
    plt.xticks(rotation=45)
    plt.show()

# (tangible) Frekans gösteren yatay bar grafiği
def create_frequency_bar_tangible(df, column_y, y_label, title):
    frequency_df = df.groupby([column_y]).size().reset_index(name='f')
    
    # Özelleştirilmiş renk paleti (her bar için farklı bir renk)
    # 'Set1', 'Set2', 'coolwarm', 'viridis'
    palette = sns.color_palette("husl", len(frequency_df))

    # Çubuk grafiği
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='f', y=column_y, data=frequency_df, orient='h', palette=palette, width=0.7)

    # Frekansları çubukların yanına doğru şekilde ekleme
    for p in ax.patches:
        width = int(p.get_width())
        position = (p.get_width(), p.get_y() + p.get_height() / 2)
        ax.annotate(f'{width}', xy=position, 
                    xytext=(-10, 0), textcoords='offset points', ha='left', va='center', 
                    color='black',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'), 
                    fontsize=14)

    # Yazı tipi boyutlarını ayarlama
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Frekans', fontdict={'weight':'bold'}, fontsize=18)
    plt.ylabel(y_label, fontdict={'weight':'bold'}, fontsize=18)
    plt.title(title, fontdict={'weight':'bold'}, fontsize=20)
    #plt.legend(title=legend_title, loc='lower right', fontsize=12, title_fontsize=14)
    
    plt.tight_layout()
    plt.show()

# Tables
def create_table(df, column_y, y_label, title):
    # Frekans verisini oluşturma
    frequency_df = df.groupby([column_y]).size().reset_index(name='f')
    
    # Yeni bir figür oluşturma
    #fig, ax = plt.subplots(figsize=(12, 6))
    fig, ax = plt.subplots()

    # Eksenleri gizleme
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    # Tabloyu oluşturma
    tabla = ax.table(cellText=frequency_df.values, colLabels=[y_label, 'Frekans'], cellLoc='center', loc='center')

    # Tablo stil ayarları
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1.2, 1.2)  # Tablo boyutlarını ölçeklendirme

    # Başlık ekleme
    plt.title(title, fontdict={'weight':'bold', 'fontsize':16})

    # Tabloyu gösterme
    plt.show()

def create_striped_table(df, column_y, y_label, title):
    # Frekans verisini oluşturma
    frequency_df = df.groupby([column_y]).size().reset_index(name='f')
    
    # Yeni bir figür oluşturma
    fig, ax = plt.subplots(figsize=(12, 6))  # Tablo boyutlarını ayarlayabilirsiniz

    # Eksenleri gizleme
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    # Tabloyu oluşturma
    tabla = ax.table(cellText=frequency_df.values, colLabels=[y_label, 'Frekans'], cellLoc='center', loc='center')

    # Tablo stil ayarları
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1.2, 1.2)  # Tablo boyutlarını ölçeklendirme

    # Satırları şeritli (striped) yapmak için renkleri ayarlama
    colors = ['#ffffff', '#e0e0e0']  # Şeritler için iki farklı renk tanımlayın
    for i in range(len(frequency_df)):
        color = colors[i % len(colors)]
        for j in range(len(frequency_df.columns)):
            tabla[(i+1, j)].set_facecolor(color)  # i+1 çünkü 0. satır başlık satırı

    # Başlık ekleme
    plt.title(title, fontdict={'weight':'bold', 'fontsize':16})

    # Tabloyu gösterme
    plt.show()

    #return fig  # fig nesnesini döndürüyoruz
