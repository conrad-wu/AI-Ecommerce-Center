from modules.content_generator import generate_amazon_title

product = {
    'brand': 'AJAZZ',
    'model': 'AK820 MAX',
    'switch': 'Magnetic Switch',
    'layout': '75%',
    'connection': 'Wired'
}

print(generate_amazon_title(product))
