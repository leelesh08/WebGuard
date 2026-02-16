# WebGuard - Automated Web Content Monitoring System

📌 **Project Overview**

WebGuard is a server-side web monitoring system designed to periodically capture and analyze specific DOM elements from web resources. The system detects structural or content-level changes by comparing newly captured data with previously stored snapshots. Upon detecting modifications, it automatically triggers an email notification.

This project demonstrates browser automation with Selenium, scheduled execution, data persistence, and differential analysis in a structured monitoring pipeline.

## 🏗 System Architecture

```
Scheduler (Interval Loop)
        ↓
Selenium (Render Page with Chrome)
        ↓
Extract Specific DOM Element (CSS Selector)
        ↓
Store Data (JSON)
        ↓
Compare with Previous Snapshot (Hash-based)
        ↓
If Changed → Send Email Alert
```

## 🛠 Tech Stack

- **Language**: Python 3.8+
- **Browser Automation**: Selenium WebDriver
- **Email**: SMTP (Gmail)
- **Data Storage**: JSON
- **Configuration**: Environment Variables (.env)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- ChromeDriver (automatically managed by Selenium in recent versions)
- Gmail account with App Password (if using Gmail for notifications)

## 🚀 Installation

1. **Clone/Download the project**
```bash
cd WebGuard
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root:
```env
TARGET_URL=https://example.com
TARGET_SELECTOR=.content-section  # CSS Selector for the element to monitor
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## ▶️ Usage

Run the monitor:
```bash
python monitor.py
```

The monitor will:
1. Check the specified URL immediately
2. Extract content from the CSS selector
3. Store the initial snapshot
4. Check every 5 minutes for changes
5. Send an email alert if changes are detected

## 📁 Project Structure

```
WebGuard/
├── monitor.py              # Main monitoring script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── data/
│   └── stored_data.json   # Snapshot storage
├── README.md              # This file
└── Stored_Data.json       # Legacy data file
```

## 🔧 Configuration

Edit the following in `monitor.py` to adjust behavior:

- `CHECK_INTERVAL`: Change monitoring frequency (default: 5 minutes = 300 seconds)
- `TARGET_URL`: Website to monitor
- `TARGET_SELECTOR`: CSS selector for the element

Or set these as environment variables in `.env`.

## 📧 Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password in your `.env` file, NOT your regular Gmail password

## ⚠️ Troubleshooting

**ChromeDriver issues:**
- Selenium should auto-handle ChromeDriver. If issues persist, install: `pip install webdriver-manager`

**Email not sending:**
- Verify Gmail 2FA is enabled and you're using an App Password
- Check firewall/proxy settings

**Element not found:**
- Verify the CSS selector is correct
- Ensure the page fully loads before the selector query

## 📝 License

MIT License

## 📧 Support

For issues or improvements, open an issue or submit a pull request.
