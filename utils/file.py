import os.path
import json

def read(file):
    text = None
    if os.path.exists(file):
        with open(file, 'r') as f:
            text = f.read()
    return text.strip()


def save(key, data):
    if not os.path.exists("cache"):
        os.makedirs("cache")
    with open("cache/" + key, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def load(key):
    if not os.path.exists("cache/" + key):
        return []
    with open("cache/" + key, 'r') as f:
        data = json.load(f)
    return data




