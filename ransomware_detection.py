import os
import smtplib
import shutil
import psutil
import time
from email.mime.text import MIMEText
from collections import Counter
import logging

logging.basicConfig(filename="C:\\Users\\(Folder_Name)\\Documents\\ransomware_log.txt", level=logging.INFO)
logging.info("Script started running")
import os
import time

MONITORED_FOLDER = "C:\\Users\\(Folder_Name)\\Documents\\MonitoredFolder"

def monitor_folder():
    print(f"Monitoring folder: {MONITORED_FOLDER}")
    while True:
        files = os.listdir(MONITORED_FOLDER)
        for file in files:
            if file.endswith(".exe") or file.endswith(".dll") or file.endswith(".locky"):  # Example: Detecting EXE/DLL files
                print(f"⚠️ Suspicious file detected: {file}")
                os.rename(
                    os.path.join(MONITORED_FOLDER, file),
                    os.path.join("C:\\Quarantine", file)
                )
                print(f"Moved {file} to quarantine.")
        time.sleep(10)  # Checks every 10 seconds


# Configuration
ALERT_EMAIL = "Enter your email"
EMAIL_PASSWORD = "Enter password"  # Use App Passwords for security
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MONITOR_DIR = "C:\\Users\\(Folder_Name)\\Documents\\MonitoredFolder"  # Change as needed
QUARANTINE_DIR = "C:\\Quarantine\\"  # Location to store suspicious files
LOG_FILE = "ransomware_log.txt"

RANSOMWARE_EXTENSIONS = {".locked", ".crypt", ".enc", ".crypto", ".encrypted", ".locky", ".ryuk", ".ransom"}

def calculate_entropy(data):
    """Calculate Shannon entropy to detect encrypted files."""
    if not data:
        return 0
    counter = Counter(data)
    length = len(data)
    entropy = -sum(count / length * (count / length).bit_length() for count in counter.values())
    return entropy

def check_file_entropy(file_path):
    """Check if a file has high entropy (potential encryption)."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return calculate_entropy(data) > 7.5  # Threshold for encryption
    except Exception:
        return False

def detect_suspicious_files():
    """Scan for ransomware files based on extension and entropy."""
    suspicious_files = []
    for root, _, files in os.walk(MONITOR_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in RANSOMWARE_EXTENSIONS or check_file_entropy(file_path):
                suspicious_files.append(file_path)
    return suspicious_files

def check_running_processes():
    """Detect suspicious processes."""
    ransomware_keywords = ["ransom", "encrypt", "locker", "decrypt"]
    suspicious_processes = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name'].lower()
            if any(keyword in process_name for keyword in ransomware_keywords):
                suspicious_processes.append((process.info['pid'], process_name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return suspicious_processes

def quarantine_file(file_path):
    """Move suspicious files to a quarantine folder."""
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    try:
        shutil.move(file_path, QUARANTINE_DIR)
        return True
    except Exception:
        return False

def kill_process(pid):
    """Kill a suspicious process."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        return True
    except Exception:
        return False

def send_email_alert(subject, message):
    """Send an email alert."""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = ALERT_EMAIL
    msg["To"] = ALERT_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(ALERT_EMAIL, EMAIL_PASSWORD)
        server.sendmail(ALERT_EMAIL, ALERT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

def log_event(event):
    """Log events to a file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")

def detect_ransomware():
    """Main function to detect and respond to ransomware."""
    print("🔍 Scanning for ransomware...\n")

    # Check for suspicious processes
    suspicious_processes = check_running_processes()
    if suspicious_processes:
        for pid, name in suspicious_processes:
            log_event(f"⚠️ Suspicious process detected: {name} (PID: {pid})")
            kill_process(pid)
        send_email_alert("🚨 Ransomware Alert!", f"Suspicious processes detected: {suspicious_processes}")

    print("✅ Scan complete. Check log file for details.")

if __name__ == "__main__":
    detect_ransomware()
    monitor_folder()
