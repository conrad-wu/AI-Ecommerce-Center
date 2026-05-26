import json
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent.parent / 'templates' / 'psd' / 'template_registry.json'


def load_registry():
    if not REGISTRY_PATH.exists():
        return {}
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_template_names():
    return list(load_registry().keys())


def get_template(name:str):
    return load_registry().get(name, {})
