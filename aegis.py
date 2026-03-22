import os, time, subprocess, requests, json, signal, sys

# --- ASCII Art Banner (نانو بانانا v2.0) ---
BANNER_LINES = [
    r"      ____ ",
    r"     /   / ",
    r"    / /_/ /___ ____  ____ ",
    r"   / __  / __ `/ __ \/ __ \ ",
    r"  / / / / /_/ / / / / /_/ / ",
    r" /_/ /_/\__,_/_/ /_/\____/ ",
    r"  Aegis EDR v2.0 - Silent Strike Labs",
    r"      [ The Stealth Shield ]",
    r"____________________________________"
]

def print_banner():
    # اختيار اللون الأحمر (31m) للبانر
    os.system("echo -e '\e[1;31m'") 
    for line in BANNER_LINES:
        print(line)
        time.sleep(0.05) # تأثير رسم البانر سطر بسطر
    os.system("echo -e '\e[0m'") # إعادة اللون الافتراضي (0m)

# --- باقي الكود الأساسي ---
def protector():
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def expand_path(p): return os.path.expanduser(p)

try:
    with open("config.json", "r") as f:
        CONF = json.load(f)
except:
    print("[-] Error: config.json missing!")
    exit()

def lockdown(reason):
    print("\n[+] AEGIS: Connection Established.\n[+] AUTHENTICATION: SUCCESS.")
    for folder in CONF["protected_folders"]:
        subprocess.run(["python", "vault_engine.py", CONF["emergency_password"], expand_path(folder)])
    
    # تصوير المخترق
    photo = expand_path("~/intruder.jpg")
    subprocess.run(["termux-camera-photo", "-c", "1", photo])
    
    # إرسال التقرير لتليجرام
    report = f"🛡️ *AEGIS SYSTEM ALERT*\nTrigger: `{reason}`\nStatus: All Data Encrypted."
    try:
        requests.post(f"https://api.telegram.org/bot{CONF['telegram_token']}/sendPhoto", 
                      files={'photo': open(photo, 'rb')}, data={'chat_id': CONF['chat_id'], 'caption': report, 'parse_mode': 'Markdown'})
    except: pass

    time.sleep(2)
    os.system("pkill -9 sshd; pkill -9 bash")

if __name__ == "__main__":
    protector()
    os.system("clear") # مسح الشاشة قبل عرض البانر
    print_banner()
    
    BAIT = expand_path(CONF["bait_directory"])
    if not os.path.exists(BAIT): os.makedirs(BAIT)
    
    last_access = os.stat(BAIT).st_mtime
    print(f"[*] Aegis Active. Monitoring: {BAIT}")

    while True:
        try:
            if os.stat(BAIT).st_mtime != last_access:
                lockdown("Unauthorized Decoy Access")
                break
            time.sleep(0.5)
        except: time.sleep(1)

