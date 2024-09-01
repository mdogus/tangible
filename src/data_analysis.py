def analyze_data(df):
    summary = df.describe()
    return summary

def save_results(df, file_path):
    df.to_csv(file_path, index=False)

# Temaları ve alt temaları oluşturma
"""
def create_themes(df, theme_prefixes, theme_names, subtheme_prefixes, subtheme_names):
    # Yeni sütunlar oluşturarak tüm satırlara varsayılan bir değer atama
    df['theme'] = 'Other'     # Diğer tüm temalar için varsayılan değer
    df['subtheme'] = 'Other'  # Diğer tüm alt temalar için varsayılan değer

    # Tüm subtheme_names'i küçük harflere dönüştürerek bir set oluşturma
    subtheme_set = {name.lower() for name in subtheme_names}

    # theme_prefixes ve theme_names kullanarak theme değerlerini güncelleme
    for prefix, theme in zip(theme_prefixes, theme_names):
        df.loc[df['tag'].str.startswith(prefix), 'theme'] = theme

    # subtheme_prefixes ve subtheme_names kullanarak subtheme değerlerini güncelleme
    for prefix, subtheme in zip(subtheme_prefixes, subtheme_names):
        # Alt tema olarak atamadan önce tag'ın subtheme_names ile aynı olup olmadığını kontrol et
        df.loc[(df['tag'].str.startswith(prefix)) & (~df['tag'].str.lower().isin(subtheme_set)), 'subtheme'] = subtheme

    return df
"""
# Temaları ve alt temaları oluşturma
def create_themes(df, theme_prefixes, theme_names, subtheme_prefixes, subtheme_names):
    # Yeni sütunlar oluşturarak varsayılan bir değer atama
    df['subtheme'] = 'Other'  # Alt temalar için varsayılan değer
    df['theme'] = 'Other'     # Temalar için varsayılan değer

    # Tüm theme_names ve subtheme_names dizilerini bir set olarak saklama
    theme_set = set(theme_names)
    subtheme_set = set(subtheme_names)

    # 1. Subtheme ataması
    for prefix, subtheme in zip(subtheme_prefixes, subtheme_names):
        # Koşul: `tag` değeri subtheme_prefixes ile başlamalı ve theme_names ile tam olarak eşleşmemeli
        df.loc[(df['tag'].str.startswith(prefix)) & (~df['tag'].isin(subtheme_set)) & (~df['tag'].isin(theme_set)), 'subtheme'] = subtheme

    # "Other" olarak tanımlanan satırları silme
    df = df[df['subtheme'] != 'Other']

    # 2. Theme ataması (subtheme'lere göre)
    for prefix, theme in zip(theme_prefixes, theme_names):
        # Koşul: `subtheme` değeri theme_prefixes ile başlamalı
        df.loc[df['subtheme'].str.startswith(prefix), 'theme'] = theme
    
    return df
