#!/usr/bin/env python3
"""
Simple test script for the registration application
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_homepage():
    """Test the homepage"""
    print("\nTesting homepage...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\nTesting user registration...")
    
    # Test data
    test_user = {
        "email": f"test_{int(time.time())}@example.com",
        "name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_duplicate_registration():
    """Test duplicate email registration"""
    print("\nTesting duplicate email registration...")
    
    test_user = {
        "email": "duplicate@example.com",
        "name": "First User"
    }
    
    try:
        # First registration
        response1 = requests.post(
            f"{BASE_URL}/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        print(f"First registration status: {response1.status_code}")
        
        # Second registration with same email
        response2 = requests.post(
            f"{BASE_URL}/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        print(f"Second registration status: {response2.status_code}")
        print(f"Second registration response: {response2.json()}")
        
        return response1.status_code == 201 and response2.status_code == 409
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_users():
    """Test getting all users"""
    print("\nTesting get users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"User count: {result.get('count', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting application tests...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Homepage", test_homepage),
        ("User Registration", test_user_registration),
        ("Duplicate Registration", test_duplicate_registration),
        ("Get Users", test_get_users)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the application logs.")

if __name__ == "__main__":
    main()
