# WebGuard
Automated Web Content Integrity &amp; Change Detection System
📌 Project Overview

Web Sentinel is a server-side web monitoring system designed to periodically capture and analyze specific DOM elements from authorized web resources. The system detects structural or content-level changes by comparing newly captured data with previously stored snapshots. Upon detecting modifications, it automatically triggers an email notification.

This project demonstrates browser automation, scheduled execution, data persistence, and differential analysis in a structured monitoring pipeline.

🏗 System Architecture

Scheduler (cron / loop)
        ↓
Puppeteer (Render JS site)
        ↓
Extract Specific DOM Element
        ↓
Store Data (JSON / SQLite)
        ↓
Compare with Previous Snapshot
        ↓
If Changed → Send Email Alert
