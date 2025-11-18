from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from app.config import DATA_DIR

def read_json(filename: str, default: Any = None) -> Any:
    """Read JSON file from data directory"""
    try:
        path = DATA_DIR / filename
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return default

def write_json(filename: str, data: Any):
    """Write data to JSON file in data directory"""
    try:
        path = DATA_DIR / filename
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing {filename}: {e}")
