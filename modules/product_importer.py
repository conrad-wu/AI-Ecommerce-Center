import pandas as pd
from modules.product_database import PRODUCT_FIELDS, upsert_product


def _clean(value):
    if pd.isna(value):
        return ''
    return str(value).strip()


def import_products_from_excel(input_file: str):
    df = pd.read_excel(input_file)
    df.columns = [str(col).strip().lower() for col in df.columns]

    imported = []
    for _, row in df.iterrows():
        product = {field: _clean(row.get(field, '')) for field in PRODUCT_FIELDS}
        sku = upsert_product(product)
        imported.append(sku)

    return imported


def create_product_import_template(output_file: str):
    sample = pd.DataFrame([
        {
            'sku': 'AK820MAX-DE-GWY',
            'brand': 'AJAZZ',
            'model': 'AK820 MAX',
            'category': 'Keyboard',
            'layout': '75%',
            'switch': 'Magnetic Switch',
            'connection': 'Wired',
            'language': 'German QWERTZ',
            'color': 'Grey White Yellow',
            'battery': 'N/A',
            'rgb': 'RGB',
            'weight': '',
            'dimensions': '',
            'platform': 'Amazon',
            'notes': 'Sample product for import'
        }
    ])
    sample.to_excel(output_file, index=False)
    return output_file
