def generate_amazon_title(product: dict) -> str:
    return (
        f"{product['brand']} {product['model']} Wireless Mechanical Keyboard, "
        f"{product['layout']} Layout, {product['switch']}, {product['connection']}"
    )
