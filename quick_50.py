python reliable_vote.py"""
FAST 50 VOTES - Keeps going until 50 successful votes achieved
"""

import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_vote(team_id, vote_num):
    """Send a single vote"""
    SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxbWXLLKTgzI7zdXklbLKuzwd-1rOT7PwabrSwjplo1_2Pvh1VbCIHOsM3LMUkfEkNHzA/exec"
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://techxhibit.vercel.app',
        'Referer': 'https://techxhibit.vercel.app/',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Microsoft Edge";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site'
    }
    
    data = {
        'action': 'vote',
        'teamId': team_id
    }
    
    try:
        response = requests.post(SCRIPT_URL, data=data, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code in [200, 302]:
            return True
        else:
            return False
    except:
        return False


def rapid_50_votes(team_id):
    """
    Keep sending votes until 50 successful votes achieved
    """
    
    print("\n" + "="*70)
    print("   RAPID 50 VOTES MODE")
    print("="*70)
    print(f"\n🎯 Target: Team {team_id}")
    print(f"🚀 Goal: 50 successful votes")
    print(f"⚡ Mode: Parallel multi-threaded")
    print(f"🔄 Will keep trying until 50 successful votes achieved")
    
    response = input(f"\n▶️  Start rapid voting? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Cancelled")
        return
    
    print("\n" + "="*70)
    print("   SENDING VOTES...")
    print("="*70 + "\n")
    
    start_time = time.time()
    success_count = 0
    total_attempts = 0
    batch_num = 0
    
    # Keep sending in batches until we reach 50 successful
    while success_count < 50:
        batch_num += 1
        
        # Calculate how many we need
        remaining = 50 - success_count
        batch_size = min(30, remaining + 10)  # Send a bit extra to account for failures
        
        print(f"\n📦 Batch {batch_num}: Sending {batch_size} votes (Need {remaining} more successful)")
        
        batch_success = 0
        
        # Send this batch in parallel
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(send_vote, team_id, total_attempts + i) for i in range(1, batch_size + 1)]
            
            for future in as_completed(futures):
                total_attempts += 1
                if future.result():
                    success_count += 1
                    batch_success += 1
                    print(f"✓ {success_count}/50 successful votes", end='\r')
                    
                    # Stop if we reached 50
                    if success_count >= 50:
                        break
        
        print(f"\n   Batch {batch_num}: {batch_success} successful")
        
        # Small delay between batches if needed
        if success_count < 50:
            time.sleep(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*70)
    print("   🎉 TARGET ACHIEVED!")
    print("="*70)
    print(f"\n📊 Final Results:")
    print(f"   ✅ Successful Votes: {success_count}")
    print(f"   📈 Total Attempts: {total_attempts}")
    print(f"   📊 Success Rate: {(success_count/total_attempts*100):.1f}%")
    print(f"   🔄 Batches: {batch_num}")
    print(f"   ⏱️  Time: {duration:.2f} seconds")
    print(f"   ⚡ Speed: {success_count/duration:.1f} votes/second")
    print(f"   🎯 Team {team_id} received 50 votes!")
    print("="*70 + "\n")


if __name__ == "__main__":
    TEAM_ID = "S19"
    rapid_50_votes(TEAM_ID)
