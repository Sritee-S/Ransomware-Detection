# Ransomware-Detection

This Python-based script is designed to monitor folders, detect suspicious ransomware behavior, and automatically respond to threats in real time. It uses techniques such as entropy analysis, process scanning, file extension monitoring, and email alerts to help identify and mitigate ransomware attacks.

Features:
1. Real-time folder monitoring for suspicious file types (.exe, .dll, .locky, etc.)
2. Detection of encrypted files using Shannon entropy
3. Scans active processes for ransomware-related keywords (e.g., encrypt, ransom)
4. Automatic quarantine of suspicious files
5. Sends email alerts on detection events
6. Logs all events and actions to a local log file

Key Components:
1. monitor_folder() – Continuously watches for suspicious files in a given folder.
2. detect_ransomware() – Scans for encrypted files and malicious processes.
3. quarantine_file() – Moves detected threats to a safe quarantine directory.
4. send_email_alert() – Notifies the user of potential ransomware activity.

Setup:
1. Update paths for MONITORED_FOLDER and QUARANTINE_DIR

2. Use a valid email & app password in the config section for alerts

3. Install required packages: psutil, smtplib, shutil
