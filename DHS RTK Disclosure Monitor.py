#!/usr/bin/env python3
# Carter's RTK Disclosure Monitor - OPSEC-friendly
# Description: Monitors a generic agency webpage or disclosure log for changes or new keywords.
# Run: python3 dhs_rtk_monitor.py

import requests
from bs4 import BeautifulSoup
import hashlib
import time
import os

# Configuration
TARGET_URL = "https://www.dhs.pa.gov/about/Pages/RTK.aspx" # Replace with specific DHS reading room/log if available
KEYWORDS = ["audit", "MCO", "financial", "MLR", "solvency"]
CHECK_INTERVAL_SECONDS = 3600 # Check every hour
HASH_FILE = "dhs_page_hash.txt"

def get_page_content():
    """Fetches the webpage securely, masquerading as a standard browser."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"🦆 [Error] Failed to fetch page: {e}")
        return None

def check_for_keywords(text):
    """Scans the page text for our target keywords."""
    found = []
    text_lower = text.lower()
    for kw in KEYWORDS:
        if kw.lower() in text_lower:
            found.append(kw)
    return found

def main():
    print("🦆 Carter's Monitor activated. Watching for RTK updates...")
    
    while True:
        html = get_page_content()
        if not html:
            time.sleep(CHECK_INTERVAL_SECONDS)
            continue
            
        soup = BeautifulSoup(html, 'html.parser')
        # Extract just the text to avoid tripping hashes on dynamic hidden tokens
        page_text = soup.get_text()
        current_hash = hashlib.md5(page_text.encode('utf-8')).hexdigest()
        
        # Load previous hash
        previous_hash = ""
        if os.path.exists(HASH_FILE):
            with open(HASH_FILE, "r") as f:
                previous_hash = f.read().strip()
                
        if current_hash != previous_hash:
            print(f"\n🚨 [ALERT] Change detected on DHS RTK page at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for specific keywords
            found_keywords = check_for_keywords(page_text)
            if found_keywords:
                print(f"🎯 Keywords found: {', '.join(found_keywords)}")
            else:
                print("ℹ️ Page updated, but no tracked keywords were found.")
                
            # Update hash
            with open(HASH_FILE, "w") as f:
                f.write(current_hash)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] No changes detected. Still hiding in the reeds...")
            
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()