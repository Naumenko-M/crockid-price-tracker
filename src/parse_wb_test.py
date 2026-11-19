import pandas as pd
import json

from wb_private_api import WBPrivateAPI
from db import save_to_sqlite

# Создаём клиент
api = WBPrivateAPI()

# Ищем товары
print("Ищу товары Crockid на Wildberries...")
catalog = api.search("Crockid")
products = catalog.products

print(f"Всего товаров: {catalog.total_products}")
print(f"На этой странице: {len(products)}\n")


# Собираем данные в список словарей
rows = []
for p in products:
    raw = p.raw if isinstance(p.raw, dict) else {}
    article = raw.get('id')

    # Собираем все размеры с ценами product и basic
    sizes_list = []
    for s in raw.get('sizes', []):
        prod = s.get('price', {}).get('product')
        basic = s.get('price', {}).get('basic')
        sizes_list.append({
            'size': s.get('name'),
            'product': prod / 100 if prod else None,
            'basic': basic / 100 if basic else None,
        })

    # Минимальный product и соответствующий basic среди размеров
    if sizes_list:
        best = min(sizes_list, key=lambda x: x['product'] if x['product'] else float('inf'))
        min_product = best['product']
        min_basic = best['basic']
    else:
        min_product = None
        min_basic = None

    # Извлекаем цвет товара и сохраняем в json
    colors = raw.get('colors') or []
    colors_names = [c.get('name') for c in colors if c.get('name')]
    colors_json = json.dumps(colors_names, ensure_ascii=False)

    rows.append({
        'article': article,
        'name': raw.get('name'),
        'brand': raw.get('brand'),
        'colors_json': colors_json,
        'price': min_product,
        'basic_price': min_basic,
        'sizes_json': json.dumps(sizes_list, ensure_ascii=False),
        'sizes_count': len(sizes_list),
        'supplier': raw.get('supplier'),
        'rating': raw.get('reviewRating'),
        'feedbacks': raw.get('feedbacks'),
    })

# Превращаем в DataFrame
df = pd.DataFrame(rows)

# Выводим результат
print(df.head())

# Диагностика
print("Всего строк:", len(df))
print("Уникальных артикулов:", df['article'].nunique())
print("Пустых артикулов:", df['article'].isna().sum())
print("Бренды:")
print(df['brand'].value_counts().head(10))

# Оставляем только Crockid
df = df[df['brand'].str.contains('Crockid', case=False, na=False)]

# Убираем дубликаты по артикулу (оставляем первую запись)
df = df.drop_duplicates(subset=['article'], keep='first')

print(f"После очистки: {len(df)} строк")

# Сохраняем в CSV
df.to_csv('data/wb_clean.csv', index=False)
print("Сохранено в data/wb_clean.csv")

# Сохраняем в SQLite
save_to_sqlite(df)