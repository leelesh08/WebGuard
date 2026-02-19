"""
WebGuard - Automated Web Content Monitoring System
Monitor specific DOM elements for changes using Selenium
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================
# Environment Variables
# ============================

load_dotenv()
TARGET_URL = os.getenv("TARGET_URL")
TARGET_SELECTOR = os.getenv("TARGET_SELECTOR")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
CHECK_INTERVAL = 60 * 60  # 1 hour in seconds

# ============================
# File Path Setup
# ============================

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "stored_data.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


# ============================
# Hash Function
# ============================

def generate_hash(data):
    """Generate SHA256 hash of data for comparison"""
    return hashlib.sha256(data.encode()).hexdigest()


# ============================
# Load Previous Snapshot
# ============================

def load_previous_snapshot():
    """Load the previously stored snapshot from JSON file"""
    if not DATA_FILE.exists():
        return None
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# ============================
# Save Snapshot
# ============================

def save_snapshot(content, hash_value):
    """Save current snapshot with timestamp and hash"""
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "content": content,
        "hash": hash_value
    }
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)


# ============================
# Send Email Alert
# ============================

def send_email_alert(new_content):
    """Send email notification when content changes are detected"""
    try:
        # Setup email server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "WebGuard Alert - Content Changed"
        message["From"] = EMAIL_USER
        message["To"] = EMAIL_USER
        
        # Email body
        body = f"""
Website Change Detected

Time: {datetime.now().isoformat()}

New Content:
{new_content}
"""
        
        message.attach(MIMEText(body, "plain"))
        
        # Send email
        server.sendmail(EMAIL_USER, EMAIL_USER, message.as_string())
        server.quit()
        
        print("📧 Email Alert Sent")
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


# ============================
# Fetch DOM Content
# ============================

def fetch_dom_content():
    """Fetch specific DOM element content using Selenium"""
    
    # Initialize Chrome driver
    options = webdriver.ChromeOptions()
    # Uncomment the line below to run in headless mode
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to URL
        print(f" Navigating to {TARGET_URL}")
        driver.get(TARGET_URL)
        
        # Wait for element to be present
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, TARGET_SELECTOR))
        )
        
        # Extract text content
        content = element.text.strip()
        
        return content
        
    except Exception as e:
        print(f"Error fetching DOM content: {str(e)}")
        raise
        
    finally:
        driver.quit()


# ============================
# Monitoring Logic
# ============================

def monitor():
    """Main monitoring function"""
    
    try:
        print(" Checking for updates...")
        
        # Fetch new content
        new_content = fetch_dom_content()
        new_hash = generate_hash(new_content)
        
        # Load previous snapshot
        previous_snapshot = load_previous_snapshot()
        
        if not previous_snapshot:
            print(" No previous snapshot found. Saving initial state.")
            save_snapshot(new_content, new_hash)
            return
        
        # Compare hashes
        if new_hash != previous_snapshot.get("hash"):
            print("  Change detected!")
            save_snapshot(new_content, new_hash)
            send_email_alert(new_content)
        else:
            print("No change detected.")
            
    except Exception as e:
        print(f" Error occurred: {str(e)}")


# ============================
# Scheduler
# ============================

if __name__ == "__main__":
    print(" WebGuard Monitor Started")
    
    # Run immediately
    monitor()
    
    # Schedule periodic checks
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            monitor()
    except KeyboardInterrupt:
        print("\nMonitor stopped by user")
