import json
import os
from pathlib import Path

def load_json_data(filename):
    """Load JSON data from the data directory"""
    try:
        data_path = Path(__file__).parent / 'data' / filename
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        return {}

def save_json_data(filename, data):
    """Save JSON data to the data directory"""
    try:
        data_path = Path(__file__).parent / 'data' / filename
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        return False
