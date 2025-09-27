#!/usr/bin/env python3
import requests
import time

def test_agent_endpoints():
    """Test if agents are actually listening"""
    
    endpoints = [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001", 
        "http://127.0.0.1:8002"
    ]
    
    for endpoint in endpoints:
        print(f"🔍 Testing {endpoint}...")
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"   ✅ Response: {response.status_code} - {response.text[:100]}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection refused")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing agent connectivity...")
    test_agent_endpoints()
    
    print("\n🔄 Testing again in 10 seconds...")
    time.sleep(10)
    test_agent_endpoints()
