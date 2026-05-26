import json
from pathlib import Path


LIBRARY_PATH = Path(__file__).resolve().parent.parent / 'data' / 'product_library.json'


def load_product_library() -> dict:
    if not LIBRARY_PATH.exists():
        return {}
    with open(LIBRARY_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_product_names():
    return list(load_product_library().keys())


def get_product_by_name(name: str) -> dict:
    return load_product_library().get(name, {})
