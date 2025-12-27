# CTF Login Bruteforcer

A Python-based brute force tool designed for CTF (Capture The Flag) competitions. This script automates login attempts with CSRF token handling, IP spoofing, and customizable parameters.

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED CTF USE ONLY**

This tool is intended exclusively for:
- Capture The Flag (CTF) competitions
- Authorized penetration testing
- Educational security research with proper authorization

**Unauthorized access to computer systems is illegal.** Only use this tool on systems you own or have explicit written permission to test.

## ✨ Features

- 🎯 **Automated Brute Force**: Username/password combination testing
- 🛡️ **CSRF Token Handling**: Automatically extracts and submits hidden form tokens
- 🌐 **IP Spoofing**: Randomized X-Forwarded-For headers to evade rate limiting
- 🔍 **Protocol Detection**: Auto-detects HTTP/HTTPS
- 🎨 **Colored Output**: Easy-to-read terminal feedback
- ⚙️ **Customizable**: Configure field names, delays, and success indicators
- 🔄 **Session Management**: Maintains cookies across requests

## 📋 Requirements

- Python 3.12+
- Required libraries:
  ```bash
  pip install requests beautifulsoup4 termcolor
  ```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Christian93111/ctf-login-bruteforcer.git
   cd ctf-login-bruteforcer.git
   ```

## 📖 Usage

Run the script:
```bash
python login_brute_ctf.py
```

You'll be prompted for:
- **Target URL**: The login page URL (e.g., `example.com/login`)
- **Username**: Target username to test
- **Wordlist Path**: Path to password wordlist file
- **Delay**: Seconds between attempts (default: 1)
- **HTML Field Names**: Form input names (defaults: `username`, `password`)

### Example Session

```
[+] Enter Target Url: ctf.example.com/login
[+] Enter Username: admin
[+] Enter Wordlist Path: /path/to/rockyou.txt
[+] Enter delay between attempts (seconds) (default: 1): 0.5
[+] HTML Field Name for User (default: username): 
[+] HTML Field Name for Pass (default: password): 

[*] Target: https://ctf.example.com/login
[*] User: admin
[*] Fields: username / password
[*] Delay: 0.5 seconds

[-] Trying: password123        | IP: 192.168.1.42
```

## 🎯 Success Detection

The script checks for these flag formats in the response:
- `flag{...}`
- `H4G{...}`
- `H5G{...}`

Modify `success_strings` in the code to match your CTF's flag format.

## ⚙️ Configuration

### Custom Field Names
If the login form uses different input names:
```
[+] HTML Field Name for User: email
[+] HTML Field Name for Pass: passwd
```

### Custom Headers
Edit `base_headers` in the code to modify User-Agent or add additional headers.

### Success Indicators
Modify the `success_strings` list to detect different success patterns:
```python
success_strings = ["flag{", "CTF{", "Welcome", "Dashboard"]
```

## 📁 Wordlists

Popular wordlists for CTF challenges:
- [SecLists](https://github.com/danielmiessler/SecLists)
- [RockYou](https://github.com/brannondorsey/naive-hashcat/releases)
- Custom CTF-specific wordlists

## 🔧 Technical Details

### CSRF Protection Bypass
The script automatically:
1. Performs GET request to fetch the login page
2. Parses HTML for hidden input fields
3. Includes all hidden tokens in POST payload

### IP Spoofing
Randomizes these headers per request:
- `X-Forwarded-For`
- `X-Client-IP`

**Note**: Effectiveness depends on server configuration. Many servers ignore these headers.

## 🛑 Limitations

- **Rate Limiting**: May not bypass sophisticated rate limiting
- **CAPTCHA**: Cannot bypass CAPTCHA challenges
- **WAF/IDS**: May be detected by Web Application Firewalls
- **Account Lockout**: Target may implement account lockout policies

## 📧 Contact

For questions or issues, please open a GitHub issue or contact the maintainer.

---

**Remember**: Always obtain proper authorization before testing any system. Ethical hacking requires ethics first.
