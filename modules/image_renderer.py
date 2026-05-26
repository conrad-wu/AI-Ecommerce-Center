from pathlib import Path
from PIL import Image, ImageDraw


def render_preview_images(product: dict, output_dir: str):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    model = product.get('model', 'Product')
    title = f"{product.get('brand', '')} {model}".strip()

    files = []

    for index, name in enumerate([
        'Amazon_Main_1.jpg',
        'Amazon_Main_2.jpg',
        'Amazon_Aplus_1.jpg'
    ]):
        image = Image.new('RGB', (1600, 1600), color=(245, 245, 245))
        draw = ImageDraw.Draw(image)

        draw.rectangle((80, 80, 1520, 1520), outline=(80, 80, 80), width=3)
        draw.text((120, 120), title, fill=(0, 0, 0))
        draw.text((120, 200), f'Template Preview #{index + 1}', fill=(0, 0, 0))
        draw.text((120, 260), f'Switch: {product.get("switch", "")}', fill=(0, 0, 0))
        draw.text((120, 320), f'Layout: {product.get("layout", "")}', fill=(0, 0, 0))

        path = output / name
        image.save(path, quality=95)
        files.append(str(path))

    return files
