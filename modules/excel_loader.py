import pandas as pd


def load_products_from_excel(input_file: str):
    df = pd.read_excel(input_file)
    df.columns = [str(col).strip().lower() for col in df.columns]

    products = []
    for _, row in df.iterrows():
        product = {}
        for key in ['sku', 'brand', 'model', 'layout', 'switch', 'connection', 'language', 'color', 'battery', 'rgb', 'platform']:
            value = row.get(key, '')
            if pd.isna(value):
                value = ''
            product[key] = str(value).strip()
        products.append(product)

    return products
