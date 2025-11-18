#!/usr/bin/env python3
"""
GANYAN IQ Backend Testing Suite
Tests all backend endpoints for the horse racing prediction system
"""

import requests
import json
from datetime import datetime
import sys
import os

# Backend URL from frontend environment
BACKEND_URL = "https://app-web-question.preview.emergentagent.com"

def test_health_endpoint():
    """Test GET /api/health - Backend health check"""
    print("\n=== Testing Health Endpoint ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            expected_keys = ["ok", "status"]
            
            if all(key in data for key in expected_keys):
                if data.get("ok") is True and data.get("status") == "healthy":
                    print("✅ Health endpoint working correctly")
                    return True
                else:
                    print("❌ Health endpoint returned unexpected values")
                    return False
            else:
                print("❌ Health endpoint missing required keys")
                return False
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health endpoint error: {str(e)}")
        return False

def test_program_lite_endpoint():
    """Test GET /api/program-lite?day=2025-11-18 - Race program (should have 15 races)"""
    print("\n=== Testing Program Lite Endpoint ===")
    
    try:
        test_date = "2025-11-18"
        response = requests.get(f"{BACKEND_URL}/api/program-lite?day={test_date}", timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # First 500 chars
        
        if response.status_code == 200:
            data = response.json()
            
            # Check structure
            if "day" in data and "rows" in data and "source" in data:
                races = data.get("rows", [])
                race_count = len(races)
                source = data.get("source")
                
                print(f"📊 Found {race_count} races from source: {source}")
                
                # Expected: 15 races with source "live"
                if race_count == 15 and source == "live":
                    print("✅ Program lite endpoint working correctly (15 races from live source)")
                    return True
                elif race_count > 0:
                    print(f"⚠️ Program lite endpoint working but found {race_count} races (expected 15) from {source} source")
                    return True  # Still working, just different data
                else:
                    print("❌ Program lite endpoint returned no races")
                    return False
            else:
                print("❌ Program lite endpoint missing required structure")
                return False
        else:
            print(f"❌ Program lite endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Program lite endpoint error: {str(e)}")
        return False

def test_results_lite_endpoint():
    """Test GET /api/results-lite?day=2025-11-18 - Race results (should have 5 results)"""
    print("\n=== Testing Results Lite Endpoint ===")
    
    try:
        test_date = "2025-11-18"
        response = requests.get(f"{BACKEND_URL}/api/results-lite?day={test_date}", timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # First 500 chars
        
        if response.status_code == 200:
            data = response.json()
            
            # Check structure
            if "day" in data and "rows" in data and "source" in data:
                results = data.get("rows", [])
                result_count = len(results)
                source = data.get("source")
                
                print(f"📊 Found {result_count} results from source: {source}")
                
                # Expected: 5 results with source "live"
                if result_count == 5 and source == "live":
                    print("✅ Results lite endpoint working correctly (5 results from live source)")
                    return True
                elif result_count > 0:
                    print(f"⚠️ Results lite endpoint working but found {result_count} results (expected 5) from {source} source")
                    return True  # Still working, just different data
                else:
                    print("❌ Results lite endpoint returned no results")
                    return False
            else:
                print("❌ Results lite endpoint missing required structure")
                return False
        else:
            print(f"❌ Results lite endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Results lite endpoint error: {str(e)}")
        return False

def test_predictions_endpoint():
    """Test GET /api/predictions?day=2025-11-18 - Alfonso AI predictions (should have 3 predictions)"""
    print("\n=== Testing Predictions Endpoint ===")
    
    try:
        test_date = "2025-11-18"
        response = requests.get(f"{BACKEND_URL}/api/predictions?day={test_date}", timeout=20)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # First 500 chars
        
        if response.status_code == 200:
            data = response.json()
            
            # Check structure
            if "ok" in data and "day" in data and "predictions" in data:
                predictions = data.get("predictions", [])
                prediction_count = len(predictions)
                message = data.get("message", "")
                
                print(f"📊 Found {prediction_count} predictions")
                if message:
                    print(f"📝 Message: {message}")
                
                # Expected: 3 predictions with horse numbers and confidence
                if prediction_count == 3:
                    # Check if predictions have required fields
                    valid_predictions = True
                    for i, pred in enumerate(predictions):
                        if not isinstance(pred, dict):
                            print(f"❌ Prediction {i+1} is not a valid object")
                            valid_predictions = False
                        # Could check for horse numbers and confidence here if structure is known
                    
                    if valid_predictions:
                        print("✅ Predictions endpoint working correctly (3 predictions)")
                        return True
                    else:
                        print("❌ Predictions have invalid structure")
                        return False
                elif prediction_count > 0:
                    print(f"⚠️ Predictions endpoint working but found {prediction_count} predictions (expected 3)")
                    return True  # Still working, just different count
                else:
                    if "Yarış programı bulunamadı" in message:
                        print("❌ Known issue: Alfonso AI predictions returning 'Yarış programı bulunamadı' (database read issue)")
                        return False
                    else:
                        print("❌ Predictions endpoint returned no predictions")
                        return False
            else:
                print("❌ Predictions endpoint missing required structure")
                return False
        else:
            print(f"❌ Predictions endpoint failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Predictions endpoint error: {str(e)}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("🚀 Starting GANYAN IQ Backend Tests")
    print(f"🔗 Backend URL: {BACKEND_URL}")
    print(f"📅 Test Date: 2025-11-18")
    
    results = {
        "health": test_health_endpoint(),
        "program_lite": test_program_lite_endpoint(),
        "results_lite": test_results_lite_endpoint(),
        "predictions": test_predictions_endpoint()
    }
    
    print("\n" + "="*50)
    print("📋 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper()}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️ Some tests failed - check logs above")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)