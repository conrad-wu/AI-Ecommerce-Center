import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'products.db'

PRODUCT_FIELDS = [
    'sku', 'brand', 'model', 'category', 'layout', 'switch', 'connection',
    'language', 'color', 'battery', 'rgb', 'weight', 'dimensions', 'platform', 'notes'
]


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            brand TEXT,
            model TEXT,
            category TEXT,
            layout TEXT,
            switch TEXT,
            connection TEXT,
            language TEXT,
            color TEXT,
            battery TEXT,
            rgb TEXT,
            weight TEXT,
            dimensions TEXT,
            platform TEXT,
            notes TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def upsert_product(product: dict):
    init_database()
    data = {field: str(product.get(field, '')).strip() for field in PRODUCT_FIELDS}
    if not data['sku']:
        data['sku'] = f"{data['brand']}-{data['model']}-{data['color']}".replace(' ', '_')

    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(PRODUCT_FIELDS))
    update_clause = ', '.join([f'{field}=excluded.{field}' for field in PRODUCT_FIELDS if field != 'sku'])
    cursor.execute(
        f'''
        INSERT INTO products ({', '.join(PRODUCT_FIELDS)})
        VALUES ({placeholders})
        ON CONFLICT(sku) DO UPDATE SET {update_clause}
        ''',
        [data[field] for field in PRODUCT_FIELDS]
    )
    conn.commit()
    conn.close()
    return data['sku']


def list_products():
    init_database()
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY brand, model, sku')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def find_product_by_sku(sku: str):
    init_database()
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE sku = ?', (sku,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_products(keyword: str):
    init_database()
    keyword = f'%{keyword}%'
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM products
        WHERE sku LIKE ? OR brand LIKE ? OR model LIKE ? OR category LIKE ? OR notes LIKE ?
        ORDER BY brand, model, sku
        ''',
        (keyword, keyword, keyword, keyword, keyword)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
