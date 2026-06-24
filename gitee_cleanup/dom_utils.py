import re
import os
from bs4 import BeautifulSoup
from .config import Config

def find_element_ancestors(selector_type, selector_val, max_levels=8):
    config = Config()
    html_path = config.html
    
    print(f"Parsing HTML file from: {html_path}")
    if not os.path.exists(html_path):
        print(f"Error: HTML file does not exist at {html_path}")
        return
        
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    if selector_type == "alt":
        el = soup.find("img", alt=selector_val)
    elif selector_type == "text":
        el = soup.find(string=lambda t: t and selector_val in t)
    elif selector_type == "class":
        el = soup.find(class_=selector_val)
    else:
        el = soup.find(selector_val)
        
    if not el:
        print(f"Element matching {selector_type}='{selector_val}' not found.")
        return

    print(f"\n--- Ancestors for {selector_type}='{selector_val}' ---")
    current = el
    level = 0
    while current and level < max_levels:
        attrs = {k: v for k, v in current.attrs.items()}
        if "class" in attrs and isinstance(attrs["class"], list):
            attrs["class"] = " ".join(attrs["class"])
        print(f"Level {level}: <{current.name} class='{attrs.get('class', '')}' id='{attrs.get('id', '')}'>")
        current = current.parent
        level += 1

def print_text_context(keyword, window_size=200):
    config = Config()
    html_path = config.html
    
    print(f"Reading HTML file from: {html_path}")
    if not os.path.exists(html_path):
        print(f"Error: HTML file does not exist at {html_path}")
        return
        
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    cleaned = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
    cleaned = re.sub(r'<style.*?>.*?</style>', '', cleaned, flags=re.DOTALL)
    
    matches = [m.start() for m in re.finditer(keyword, cleaned)]
    print(f"Found {len(matches)} occurrences of '{keyword}' outside scripts/styles.")
    for idx, pos in enumerate(matches):
        start = max(0, pos - window_size)
        end = min(len(cleaned), pos + window_size)
        print(f"Match #{idx}:")
        print(cleaned[start:end])
        print("-" * 50)
