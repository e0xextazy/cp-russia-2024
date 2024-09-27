import json

FAQ_FILE = 'faq.json'


def load_faq():
    with open(FAQ_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_faq(data):
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
