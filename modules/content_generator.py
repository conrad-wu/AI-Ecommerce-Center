from datetime import datetime


def _value(product: dict, key: str, default: str = '') -> str:
    return str(product.get(key, default)).strip()


def generate_amazon_title(product: dict) -> str:
    brand = _value(product, 'brand', 'AJAZZ')
    model = _value(product, 'model', 'Keyboard')
    layout = _value(product, 'layout', '75%')
    switch = _value(product, 'switch', 'Mechanical Switch')
    connection = _value(product, 'connection', 'USB-C')
    language = _value(product, 'language', 'US Layout')
    color = _value(product, 'color', '')
    color_part = f', {color}' if color else ''
    return f'{brand} {model} Mechanical Gaming Keyboard, {layout} Layout, {switch}, {connection}, {language}{color_part}'


def generate_bullets(product: dict):
    return [
        f"{_value(product, 'switch', 'Mechanical Switch')} delivers fast response and satisfying typing feedback.",
        f"Compact {_value(product, 'layout', '75%')} layout saves desk space while keeping essential keys for work and gaming.",
        f"{_value(product, 'connection', 'USB-C')} connection provides stable performance for daily use and competitive gaming.",
        f"{_value(product, 'rgb', 'RGB lighting')} creates a clean desktop atmosphere and enhances the gaming setup.",
        f"Designed for {_value(product, 'platform', 'Amazon / TEMU / TikTok Shop')} users who want performance, style and value in one keyboard."
    ]


def generate_description(product: dict) -> str:
    return (
        f"The {_value(product, 'brand', 'AJAZZ')} {_value(product, 'model', 'keyboard')} is designed for gamers, office users and setup enthusiasts. "
        f"With a {_value(product, 'layout', '75%')} layout, {_value(product, 'switch', 'mechanical switch')} and {_value(product, 'connection', 'USB-C')} connectivity, "
        "it balances performance, comfort and desktop aesthetics. This product is suitable for Amazon listing, TEMU product pages and TikTok Shop short-form selling points."
    )


def generate_temu_points(product: dict):
    return [
        'High-value mechanical keyboard for daily use',
        f"{_value(product, 'layout', '75%')} compact design",
        f"{_value(product, 'switch', 'Mechanical Switch')} typing feel",
        'Gaming and office compatible',
        'Easy to present with clear main-image selling points'
    ]


def generate_tiktok_points(product: dict):
    return [
        'Desk setup upgrade in seconds',
        'Satisfying typing sound for short videos',
        'Gaming-ready look and feel',
        'Great for keyboard ASMR content',
        'Clean visual style for TikTok product showcases'
    ]


def generate_aplus_modules(product: dict):
    return {
        'module1_hero': f"{_value(product, 'brand', 'AJAZZ')} {_value(product, 'model', '')} | Built for Gaming, Work and Clean Desk Setups",
        'module2_switch': f"{_value(product, 'switch', 'Mechanical Switch')} | Fast Response and Smooth Typing Feel",
        'module3_layout': f"{_value(product, 'layout', '75%')} Layout | Compact Size, Practical Function",
        'module4_connection': f"{_value(product, 'connection', 'USB-C')} | Stable Connection for Daily Use",
        'module5_specs': 'Product Specifications | Layout, Switch, Connection, Lighting, Color and Compatibility'
    }


def generate_image_prompts(product: dict):
    brand = _value(product, 'brand', 'AJAZZ')
    model = _value(product, 'model', 'keyboard')
    color = _value(product, 'color', 'clean neutral color')
    return {
        'amazon_main_image': f"Create a premium Amazon main image for {brand} {model}, clean white background, product centered, sharp details, ecommerce-ready lighting, no extra logo added.",
        'aplus_hero': f"Create an Amazon A+ hero banner for {brand} {model}, modern gaming desk setup, {color} theme, premium lighting, space for English headline text.",
        'lifestyle': f"Create a lifestyle scene for {brand} {model}, European gaming desk setup, clean desktop, soft lighting, premium mechanical keyboard atmosphere.",
        'tiktok_ad': f"Create a dynamic TikTok product showcase image for {brand} {model}, trendy desk setup, keyboard close-up, energetic gaming atmosphere."
    }


def generate_markdown(product: dict) -> str:
    bullets = '\n'.join([f'- {item}' for item in generate_bullets(product)])
    temu = '\n'.join([f'- {item}' for item in generate_temu_points(product)])
    tiktok = '\n'.join([f'- {item}' for item in generate_tiktok_points(product)])
    aplus = '\n'.join([f'- **{key}**: {value}' for key, value in generate_aplus_modules(product).items()])
    image_prompts = '\n'.join([f'- **{key}**: {value}' for key, value in generate_image_prompts(product).items()])

    return f"""# AI Ecommerce Material Output

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Product Info

- Brand: {_value(product, 'brand')}
- Model: {_value(product, 'model')}
- Layout: {_value(product, 'layout')}
- Switch: {_value(product, 'switch')}
- Connection: {_value(product, 'connection')}
- Language: {_value(product, 'language')}
- Color: {_value(product, 'color')}
- Platform: {_value(product, 'platform')}

## Amazon Title

{generate_amazon_title(product)}

## Amazon Bullet Points

{bullets}

## Product Description

{generate_description(product)}

## TEMU Selling Points

{temu}

## TikTok Selling Points

{tiktok}

## Amazon A+ Modules

{aplus}

## Image Prompts

{image_prompts}
"""
