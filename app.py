from modules.content_generator import *

product = {
    'brand': 'AJAZZ',
    'model': 'AK820 MAX',
    'switch': 'Magnetic Switch',
    'layout': '75%',
    'connection': 'Wired'
}

print('\n=== AMAZON TITLE ===')
print(generate_amazon_title(product))

print('\n=== BULLETS ===')
for item in generate_bullets(product):
    print('-', item)

print('\n=== DESCRIPTION ===')
print(generate_description(product))

print('\n=== TEMU ===')
print(generate_temu_points(product))

print('\n=== TIKTOK ===')
print(generate_tiktok_points(product))

print('\n=== A+ MODULES ===')
print(generate_aplus_modules(product))
