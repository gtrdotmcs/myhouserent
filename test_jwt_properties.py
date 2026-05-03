import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_properties(username, password):
    # Get token
    auth_response = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": username, "password": password}
    )
    token = auth_response.json()["access"]
    
    # Get properties
    headers = {"Authorization": f"Bearer {token}"}
    prop_response = requests.get(
        f"{BASE_URL}/api/properties/", 
        headers=headers
    )
    
    print(f"\n{username} ({auth_response.json().get('role', 'unknown')}):")
    print(f"Status: {prop_response.status_code}")
    print(f"Properties: {len(prop_response.json())}")
    print(f"Data: {prop_response.json()}")

# Test different users
test_user_properties("admin", "adminpassword")
test_user_properties("owner1", "password123")
test_user_properties("tenant1", "password123")