const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");
const nodemailer = require("nodemailer");
const crypto = require("crypto");
require("dotenv").config();

/* ============================
   Environment Variables
============================ */

const TARGET_URL = process.env.TARGET_URL;
const TARGET_SELECTOR = process.env.TARGET_SELECTOR;
const EMAIL_USER = process.env.EMAIL_USER;
const EMAIL_PASS = process.env.EMAIL_PASS;
const CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes

/* ============================
   File Path Setup
============================ */

const DATA_DIR = path.join(__dirname, "data");
const DATA_FILE = path.join(DATA_DIR, "stored_data.json");

/* ============================
   Ensure Data Directory Exists
============================ */

if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR);
}

/* ============================
   Hash Function (Better Comparison)
============================ */

function generateHash(data) {
    return crypto.createHash("sha256").update(data).digest("hex");
}

/* ============================
   Load Previous Snapshot
============================ */

function loadPreviousSnapshot() {
    if (!fs.existsSync(DATA_FILE)) {
        return null;
    }
    const raw = fs.readFileSync(DATA_FILE);
    return JSON.parse(raw);
}

/* ============================
   Save Snapshot
============================ */

function saveSnapshot(content, hash) {
    const snapshot = {
        timestamp: new Date().toISOString(),
        content: content,
        hash: hash
    };
    fs.writeFileSync(DATA_FILE, JSON.stringify(snapshot, null, 2));
}

/* ============================
   Send Email Alert
============================ */

async function sendEmailAlert(newContent) {

    const transporter = nodemailer.createTransport({
        service: "gmail",
        auth: {
            user: EMAIL_USER,
            pass: EMAIL_PASS
        }
    });

    const message = `
Website Change Detected

Time: ${new Date().toISOString()}

New Content:
${newContent}
`;

    await transporter.sendMail({
        from: EMAIL_USER,
        to: EMAIL_USER,
        subject: "Web Sentinel Alert - Content Changed",
        text: message
    });

    console.log("📧 Email Alert Sent");
}

/* ============================
   Fetch DOM Content
============================ */

async function fetchDOMContent() {

    const browser = await puppeteer.launch({
        headless: "new",
        args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    const page = await browser.newPage();

    await page.goto(TARGET_URL, {
        waitUntil: "networkidle2"
    });

    const content = await page.$eval(
        TARGET_SELECTOR,
        el => el.innerText
    );

    await browser.close();

    return content.trim();
}

/* ============================
   Monitoring Logic
============================ */

async function monitor() {

    try {

        console.log("🔍 Checking for updates...");

        const newContent = await fetchDOMContent();
        const newHash = generateHash(newContent);

        const previousSnapshot = loadPreviousSnapshot();

        if (!previousSnapshot) {

            console.log("📁 No previous snapshot found. Saving initial state.");
            saveSnapshot(newContent, newHash);
            return;

        }

        if (newHash !== previousSnapshot.hash) {

            console.log("⚠ Change detected!");
            saveSnapshot(newContent, newHash);
            await sendEmailAlert(newContent);

        } else {

            console.log("✅ No change detected.");

        }

    } catch (error) {
        console.error("❌ Error occurred:", error.message);
    }

}

/* ============================
   Scheduler
============================ */

monitor(); // Run immediately
setInterval(monitor, CHECK_INTERVAL);