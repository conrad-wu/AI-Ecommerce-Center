import json
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parent.parent / 'templates' / 'psd' / 'template_config.json'


def load_template_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_template(template_name: str):
    config = load_template_config()
    return config.get(template_name, {})


def build_layer_payload(product: dict, bullets=None):
    bullets = bullets or []

    return {
        'TITLE': f"{product.get('brand', '')} {product.get('model', '')}".strip(),
        'SUBTITLE': product.get('switch', ''),
        'SELLING_POINT_1': bullets[0] if len(bullets) > 0 else '',
        'SELLING_POINT_2': bullets[1] if len(bullets) > 1 else '',
        'SELLING_POINT_3': bullets[2] if len(bullets) > 2 else '',
        'SELLING_POINT_4': bullets[3] if len(bullets) > 3 else '',
        'SELLING_POINT_5': bullets[4] if len(bullets) > 4 else '',
        'PRODUCT_IMAGE': 'Replace with product image path',
        'LOGO': 'Replace with logo image path'
    }
