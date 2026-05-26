import pandas as pd
from modules.content_generator import (
    generate_amazon_title,
    generate_description,
)


def process_excel(input_file: str, output_file: str):
    df = pd.read_excel(input_file)

    results = []

    for _, row in df.iterrows():
        product = {
            'brand': row.get('brand', ''),
            'model': row.get('model', ''),
            'layout': row.get('layout', ''),
            'switch': row.get('switch', ''),
            'connection': row.get('connection', ''),
            'language': row.get('language', ''),
            'color': row.get('color', ''),
            'platform': row.get('platform', ''),
        }

        results.append({
            'SKU': row.get('sku', ''),
            'Amazon Title': generate_amazon_title(product),
            'Product Description': generate_description(product),
        })

    pd.DataFrame(results).to_excel(output_file, index=False)

    return output_file
