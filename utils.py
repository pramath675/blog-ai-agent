# utils.py
import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60]

def save_markdown(folder, filename, content):
    Path(folder).mkdir(parents=True, exist_ok=True)
    path = Path(folder) / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return str(path)

def unique_filename(prefix, title):
    h = hashlib.sha1(title.encode()).hexdigest()[:8]
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}_{slugify(title)}_{ts}_{h}.md"
