#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Firefox URL Loader - 2 Windows with 5-min Auto Refresh
With Screenshot & Telegram Integration
Auto-installs all dependencies
"""

import os
import sys
import subprocess
import time

# ==================== AUTO INSTALL DEPENDENCIES ====================
def auto_install_dependencies():
    """Auto install required packages"""
    required = ['requests', 'psutil', 'pillow']
    
    print("=" * 60)
    print("CHECKING AND INSTALLING DEPENDENCIES...")
    print("=" * 60)
    
    for package in required:
        try:
            # Check if package is installed
            if package == 'pillow':
                __import__('PIL')
            else:
                __import__(package)
            print(f"[OK] {package} already installed")
        except ImportError:
            print(f"[*] Installing {package}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "--quiet"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"[OK] {package} installed successfully")
            except Exception as e:
                print(f"[FAIL] Failed to install {package}: {e}")
                # Try with --user flag
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package, "--user", "--quiet"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(f"[OK] {package} installed successfully (--user)")
                except:
                    print(f"[FAIL] Failed to install {package} even with --user flag")
                    sys.exit(1)
    
    print("=" * 60)
    print("[OK] ALL DEPENDENCIES INSTALLED")
    print("=" * 60)
    print()

# Install dependencies before importing
auto_install_dependencies()

# ==================== IMPORTS ====================
import requests
import psutil
from datetime import datetime
from PIL import ImageGrab

# ==================== CONFIG ====================
FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# URLs to open (2 URLs)
URLS = [
    "https://ais-pre-53ck2q5agt2tcwz3e52bjd-628481697275.asia-east1.run.app",
    "https://ais-pre-xymzvoid6ag4yjrlxsjvue-628481697275.asia-east1.run.app"
]

REFRESH_INTERVAL = 300  # 5 minutes in seconds

# ==================== TELEGRAM CONFIG ====================
TELEGRAM_BOT_TOKEN = "8972471605:AAE7hhT8QO5N_hnfHTIX1PxRzmkRBm5voyY"
TELEGRAM_CHAT_ID = "6955911349"

# ==================== FUNCTIONS ====================
def log(msg):
    """Print log with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def send_telegram_message(message):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            log("Telegram message sent")
        else:
            log(f"Telegram message failed: {response.status_code}")
    except Exception as e:
        log(f"Telegram error: {e}")

def send_telegram_photo(image_path, caption):
    """Send photo to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, 'rb') as f:
            files = {'photo': f}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, files=files, data=data, timeout=30)
            if response.status_code == 200:
                log("Telegram photo sent")
            else:
                log(f"Telegram photo failed: {response.status_code}")
    except Exception as e:
        log(f"Telegram photo error: {e}")
    finally:
        # Clean up screenshot
        if os.path.exists(image_path):
            os.remove(image_path)
            log("Screenshot cleaned up")

def take_screenshot(filename="screenshot.png"):
    """Take screenshot of entire screen"""
    try:
        log(f"Taking screenshot: {filename}")
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        log(f"Screenshot saved: {filename}")
        return filename
    except Exception as e:
        log(f"Screenshot failed: {e}")
        return None

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
            log(f"  FAILED to open window {i}: {e}")
    
    log("All windows opened!")

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
        log(f"Closed {closed} Firefox process(es)")
    except Exception as e:
        log(f"Error closing Firefox: {e}")

def check_firefox():
    """Check if Firefox is installed"""
    global FIREFOX_PATH
    
    if os.path.exists(FIREFOX_PATH):
        return True
    
    # Try alternative paths
    alt_paths = [
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        r"C:\Users\runneradmin\AppData\Local\Mozilla Firefox\firefox.exe"
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            FIREFOX_PATH = path
            return True
    
    return False

def get_system_info():
    """Get basic system info"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB ({ram.percent}%)"
    except:
        return "System info unavailable"

def wait_with_countdown(seconds, message):
    """Wait with countdown display"""
    log(message)
    for i in range(seconds, 0, -1):
        if i % 10 == 0 or i <= 5:
            print(f"  {i} seconds remaining...")
        time.sleep(1)

# ==================== MAIN LOOP ====================
def main():
    log("=" * 60)
    log("SIMPLE FIREFOX URL LOADER STARTED")
    log("=" * 60)
    
    # Check Firefox installation
    if not check_firefox():
        log("Firefox not found! Please install Firefox.")
        send_telegram_message("<b>ERROR</b>\nFirefox not found!")
        sys.exit(1)
    
    log(f"Firefox found at: {FIREFOX_PATH}")
    log(f"URLs to load: {len(URLS)}")
    for i, url in enumerate(URLS, 1):
        log(f"   URL {i}: {url}")
    log(f"Refresh interval: {REFRESH_INTERVAL // 60} minutes")
    log(f"System: {get_system_info()}")
    log("=" * 60)
    
    # Send startup message
    startup_msg = f"""<b>FIREFOX URL LOADER STARTED</b>

URLs: {len(URLS)}
Refresh: {REFRESH_INTERVAL // 60} minutes
{get_system_info()}

Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    send_telegram_message(startup_msg)
    
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
            
            log(f"Cycle #{cycle_count} complete!")
            
            # ===== CONFIRMATION SCREENSHOTS =====
            # Wait 10 seconds for first screenshot
            wait_with_countdown(10, "Waiting 10 seconds for first confirmation...")
            
            # Take first screenshot
            ss1 = take_screenshot("screenshot_10sec.png")
            if ss1:
                caption1 = f"""CONFIRMATION #1 - 10 SECONDS

Cycle: #{cycle_count}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{get_system_info()}

Both windows should be visible"""
                send_telegram_photo(ss1, caption1)
            
            # Wait additional 20 seconds (total 30 seconds)
            wait_with_countdown(20, "Waiting 20 more seconds for second confirmation...")
            
            # Take second screenshot
            ss2 = take_screenshot("screenshot_30sec.png")
            if ss2:
                caption2 = f"""CONFIRMATION #2 - 30 SECONDS

Cycle: #{cycle_count}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{get_system_info()}

Windows are active and running"""
                send_telegram_photo(ss2, caption2)
            
            log("Screenshots sent to Telegram!")
            
            log(f"Next refresh in {REFRESH_INTERVAL // 60} minutes...")
            log("=" * 60)
            
            # Wait before next cycle
            time.sleep(REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        log("\nScript stopped by user")
        send_telegram_message("<b>SCRIPT STOPPED</b>\nManually stopped by user")
        close_all_firefox()
        log("Cleaned up Firefox processes")
        sys.exit(0)
    except Exception as e:
        log(f"Unexpected error: {e}")
        send_telegram_message(f"<b>ERROR</b>\n{str(e)}")
        close_all_firefox()
        sys.exit(1)

if __name__ == "__main__":
    main()
