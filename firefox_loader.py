#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Firefox URL Loader - 2 Windows with 5-min Auto Refresh
"""

import os
import sys
import subprocess
import time
import psutil
from datetime import datetime

# ==================== CONFIG ====================
FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# URLs to open (2 URLs)
URLS = [
    "https://ais-pre-53ck2q5agt2tcwz3e52bjd-628481697275.asia-east1.run.app",
    "https://ais-pre-xymzvoid6ag4yjrlxsjvue-628481697275.asia-east1.run.app"
]

REFRESH_INTERVAL = 300  # 5 minutes in seconds

# ==================== FUNCTIONS ====================
def log(msg):
    """Print log with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def open_windows():
    """Open each URL in a separate Firefox window"""
    log(f"Opening {len(URLS)} Firefox windows...")
    
    for i, url in enumerate(URLS, 1):
        try:
            log(f"  Opening window {i}: {url}")
            subprocess.Popen(
                [FIREFOX_PATH, "-new-window", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(3)  # Gap between windows
        except Exception as e:
            log(f"  ❌ Failed to open window {i}: {e}")
    
    log("✅ All windows opened!")

def close_all_firefox():
    """Close all Firefox windows"""
    log("Closing all Firefox windows...")
    closed = 0
    
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'firefox' in proc.info['name'].lower():
                    proc.terminate()
                    closed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        time.sleep(2)  # Wait for processes to close
        log(f"✅ Closed {closed} Firefox process(es)")
    except Exception as e:
        log(f"❌ Error closing Firefox: {e}")

def check_firefox():
    """Check if Firefox is installed"""
    if os.path.exists(FIREFOX_PATH):
        return True
    
    # Try alternative paths
    alt_paths = [
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        r"C:\Users\runneradmin\AppData\Local\Mozilla Firefox\firefox.exe"
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            global FIREFOX_PATH
            FIREFOX_PATH = path
            return True
    
    return False

def get_system_info():
    """Get basic system info"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB"
    except:
        return "System info unavailable"

# ==================== MAIN LOOP ====================
def main():
    log("=" * 60)
    log("SIMPLE FIREFOX URL LOADER STARTED")
    log("=" * 60)
    
    # Check Firefox installation
    if not check_firefox():
        log("❌ Firefox not found! Please install Firefox.")
        log(f"   Expected at: {FIREFOX_PATH}")
        sys.exit(1)
    
    log(f"✅ Firefox found at: {FIREFOX_PATH}")
    log(f"📋 URLs to load: {len(URLS)}")
    for i, url in enumerate(URLS, 1):
        log(f"   URL {i}: {url}")
    log(f"🔄 Refresh interval: {REFRESH_INTERVAL // 60} minutes")
    log(f"💻 System: {get_system_info()}")
    log("=" * 60)
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            log(f"\n{'='*60}")
            log(f"CYCLE #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log(f"{'='*60}")
            
            # Close all Firefox windows
            close_all_firefox()
            time.sleep(2)
            
            # Open new windows
            open_windows()
            
            log(f"✅ Cycle #{cycle_count} complete!")
            log(f"⏰ Next refresh in {REFRESH_INTERVAL // 60} minutes...")
            log("=" * 60)
            
            # Wait before next cycle
            time.sleep(REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        log("\n⚠️ Script stopped by user")
        close_all_firefox()
        log("🧹 Cleaned up Firefox processes")
        sys.exit(0)
    except Exception as e:
        log(f"❌ Unexpected error: {e}")
        close_all_firefox()
        sys.exit(1)

if __name__ == "__main__":
    main()
