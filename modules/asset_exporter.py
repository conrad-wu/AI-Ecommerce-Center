import json
import re
from datetime import datetime
from pathlib import Path
from modules.content_generator import generate_image_prompts, generate_markdown


def _safe_name(text: str) -> str:
    text = text.strip() or 'product'
    text = re.sub(r'[^A-Za-z0-9_-]+', '_', text)
    return text.strip('_')


def export_material_package(product: dict, output_root: str = 'output') -> str:
    model = product.get('model', 'product')
    folder_name = _safe_name(model)
    output_dir = Path(output_root) / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown = generate_markdown(product)
    image_prompts = generate_image_prompts(product)

    listing_path = output_dir / 'listing.md'
    prompts_path = output_dir / 'image_prompts.txt'
    assets_path = output_dir / 'assets.json'

    listing_path.write_text(markdown, encoding='utf-8')

    prompts_text = '\n\n'.join([
        f'{key}:\n{value}' for key, value in image_prompts.items()
    ])
    prompts_path.write_text(prompts_text, encoding='utf-8')

    assets = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'product': product,
        'files': {
            'listing': str(listing_path),
            'image_prompts': str(prompts_path),
        },
        'psd_layer_naming_guide': {
            'product_image': 'PRODUCT_IMAGE',
            'title': 'TITLE',
            'selling_point_1': 'SELLING_POINT_1',
            'selling_point_2': 'SELLING_POINT_2',
            'selling_point_3': 'SELLING_POINT_3',
            'logo': 'LOGO',
            'background': 'BACKGROUND'
        }
    }
    assets_path.write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding='utf-8')

    return str(output_dir)
