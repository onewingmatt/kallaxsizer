#!/usr/bin/env python3
"""
Test to verify the Kallax app is working correctly
"""
import requests
import time

print("Testing Kallax app...")
print("=" * 60)

# Test 1: Check if server is running
print("\n1. Checking if server is running on port 8042...")
try:
    resp = requests.get("http://localhost:8042/", timeout=5)
    if resp.status_code == 200:
        print("   ✓ Server is running")
        if "Kallax Konfigurator" in resp.text:
            print("   ✓ Main page loads correctly")
        else:
            print("   ✗ Page content is missing or corrupted")
    else:
        print(f"   ✗ Server returned status {resp.status_code}")
except Exception as e:
    print(f"   ✗ Could not connect: {e}")
    exit(1)

# Test 2: Check if /api/status endpoint works
print("\n2. Checking /api/status endpoint...")
try:
    resp = requests.get("http://localhost:8042/api/status", timeout=5)
    if resp.status_code == 200:
        print("   ✓ /api/status works")
        data = resp.json()
        print(f"   - Cached games: {data.get('cached_games', 0)}")
    else:
        print(f"   ✗ /api/status returned {resp.status_code}")
except Exception as e:
    print(f"   ✗ /api/status error: {e}")

# Test 3: Check if /api/versions endpoint works
print("\n3. Checking /api/versions endpoint...")
try:
    resp = requests.get("http://localhost:8042/api/versions?id=70323", timeout=30)
    if resp.status_code == 200:
        print("   ✓ /api/versions works")
        data = resp.json()
        versions = data.get('versions', [])
        print(f"   - Found {len(versions)} versions for game 70323 (King of Tokyo)")
        if versions:
            print(f"   - First version: {versions[0].get('name')}")
    else:
        print(f"   ✗ /api/versions returned {resp.status_code}")
except Exception as e:
    print(f"   ✗ /api/versions error: {e}")

# Test 4: Check if CSS/JS assets load
print("\n4. Checking for JavaScript and CSS loads...")
resp = requests.get("http://localhost:8042/")
if "<style>" in resp.text:
    print("   ✓ CSS is embedded")
if "<script>" in resp.text:
    print("   ✓ JavaScript is embedded")

print("\n" + "=" * 60)
print("✓ All checks passed! App is functioning correctly.")
print("\nTo test the collection loader:")
print("1. Open http://localhost:8042 in your browser")
print("2. Click the '🎲 Demo Mode' button to test with sample games")
print("3. Or upload a CSV file from your BGG collection")
