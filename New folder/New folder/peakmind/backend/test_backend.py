import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing PeakMind AI Backend...")
    
    # 1. Health check
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {r.json()}")
    except requests.exceptions.ConnectionError:
        print("Backend server is not running! Please start it first.")
        return

    user_id = "test_user_123"

    # 2. Log Energy
    print("\n--- Logging Energy ---")
    energy_data = {
        "user_id": user_id,
        "score": 30,
        "mood": "tired"
    }
    r = requests.post(f"{BASE_URL}/api/energy/", json=energy_data)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Response: {json.dumps(r.json(), indent=2)}")

    # 3. Create Tasks
    print("\n--- Creating Tasks ---")
    tasks = [
        {"user_id": user_id, "title": "Write Next.js components", "priority": 3},
        {"user_id": user_id, "title": "Reply to emails", "priority": 1},
        {"user_id": user_id, "title": "Debug database issue", "priority": 3}
    ]
    for t in tasks:
        r = requests.post(f"{BASE_URL}/api/tasks/", json=t)
        print(f"Created Task: {r.json()['title']}")

    # 4. Get Task Priority Suggestion from AI
    print("\n--- AI Task Prioritization Suggestion ---")
    r = requests.get(f"{BASE_URL}/api/tasks/suggest-priority?user_id={user_id}")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Response: {json.dumps(r.json(), indent=2)}")

if __name__ == "__main__":
    run_tests()
