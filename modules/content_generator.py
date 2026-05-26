def generate_amazon_title(product: dict) -> str:
    return f"{product['brand']} {product['model']} Mechanical Keyboard, {product['layout']} Layout, {product['switch']}, {product['connection']}"


def generate_bullets(product: dict):
    return [
        f"Premium {product['switch']} for gaming and productivity",
        f"Compact {product['layout']} layout saves desk space",
        f"{product['connection']} connectivity for stable performance",
        "Hot-swappable design for easy customization",
        "Ideal for office, gaming and content creation"
    ]


def generate_description(product: dict) -> str:
    return (
        f"The {product['brand']} {product['model']} is designed for gamers and professionals. "
        f"Featuring a {product['layout']} layout and {product['switch']}, it delivers a smooth typing experience."
    )


def generate_temu_points(product: dict):
    return [
        'Fast response',
        'Compact layout',
        'Premium build quality',
        'Easy customization',
        'Great value for money'
    ]


def generate_tiktok_points(product: dict):
    return [
        'Perfect desk setup upgrade',
        'Satisfying typing sound',
        'Gaming-ready performance',
        'RGB-ready customization',
        'Trending mechanical keyboard'
    ]


def generate_aplus_modules(product: dict):
    return {
        'module1': 'Hero Banner + Key Selling Points',
        'module2': 'Switch Technology Overview',
        'module3': 'Connectivity & Compatibility',
        'module4': 'Typing Experience',
        'module5': 'Product Specifications'
    }
