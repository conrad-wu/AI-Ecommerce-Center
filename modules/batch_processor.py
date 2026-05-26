import pandas as pd
from modules.content_generator import (
    generate_amazon_title,
    generate_aplus_modules,
    generate_bullets,
    generate_description,
    generate_image_prompts,
    generate_temu_points,
    generate_tiktok_points,
)


INPUT_COLUMNS = [
    'sku', 'brand', 'model', 'layout', 'switch', 'connection',
    'language', 'color', 'battery', 'rgb', 'platform'
]


def _get(row, key: str) -> str:
    value = row.get(key, '')
    if pd.isna(value):
        return ''
    return str(value).strip()


def row_to_product(row) -> dict:
    return {
        'brand': _get(row, 'brand'),
        'model': _get(row, 'model'),
        'layout': _get(row, 'layout'),
        'switch': _get(row, 'switch'),
        'connection': _get(row, 'connection'),
        'language': _get(row, 'language'),
        'color': _get(row, 'color'),
        'battery': _get(row, 'battery'),
        'rgb': _get(row, 'rgb'),
        'platform': _get(row, 'platform'),
    }


def process_excel(input_file: str, output_file: str):
    df = pd.read_excel(input_file)
    df.columns = [str(col).strip().lower() for col in df.columns]

    results = []

    for _, row in df.iterrows():
        product = row_to_product(row)
        bullets = generate_bullets(product)
        aplus = generate_aplus_modules(product)
        image_prompts = generate_image_prompts(product)

        results.append({
            'SKU': _get(row, 'sku'),
            'Brand': product['brand'],
            'Model': product['model'],
            'Amazon Title': generate_amazon_title(product),
            'Bullet 1': bullets[0] if len(bullets) > 0 else '',
            'Bullet 2': bullets[1] if len(bullets) > 1 else '',
            'Bullet 3': bullets[2] if len(bullets) > 2 else '',
            'Bullet 4': bullets[3] if len(bullets) > 3 else '',
            'Bullet 5': bullets[4] if len(bullets) > 4 else '',
            'Product Description': generate_description(product),
            'TEMU Selling Points': '\n'.join(generate_temu_points(product)),
            'TikTok Selling Points': '\n'.join(generate_tiktok_points(product)),
            'A+ Module 1': aplus.get('module1_hero', ''),
            'A+ Module 2': aplus.get('module2_switch', ''),
            'A+ Module 3': aplus.get('module3_layout', ''),
            'A+ Module 4': aplus.get('module4_connection', ''),
            'A+ Module 5': aplus.get('module5_specs', ''),
            'Amazon Main Image Prompt': image_prompts.get('amazon_main_image', ''),
            'A+ Hero Prompt': image_prompts.get('aplus_hero', ''),
            'Lifestyle Prompt': image_prompts.get('lifestyle', ''),
            'TikTok Ad Prompt': image_prompts.get('tiktok_ad', ''),
        })

    pd.DataFrame(results).to_excel(output_file, index=False)
    return output_file


def create_sample_excel(output_file: str):
    sample = pd.DataFrame([
        {
            'sku': 'AK820MAX-DE-GWY',
            'brand': 'AJAZZ',
            'model': 'AK820 MAX',
            'layout': '75%',
            'switch': 'Magnetic Switch',
            'connection': 'Wired',
            'language': 'German QWERTZ',
            'color': 'Grey White Yellow',
            'battery': 'N/A',
            'rgb': 'RGB',
            'platform': 'Amazon',
        },
        {
            'sku': 'AJ139V2MC-BK',
            'brand': 'AJAZZ',
            'model': 'AJ139 V2 MC',
            'layout': 'Mouse',
            'switch': 'Gaming Mouse Switch',
            'connection': '2.4G / USB-C / Bluetooth',
            'language': 'Universal',
            'color': 'Black',
            'battery': 'Rechargeable',
            'rgb': 'No RGB',
            'platform': 'Amazon',
        },
    ])
    sample.to_excel(output_file, index=False)
    return output_file
