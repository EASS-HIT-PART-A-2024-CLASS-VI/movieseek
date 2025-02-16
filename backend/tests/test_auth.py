import pytest
import random
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def generate_random_user():
    return f"user_{random.randint(1000, 9999)}"

def test_register_user():
    """
    Test user registration with a unique username.
    """
    username = generate_random_user()
    response = client.post("/register", json={"username": username, "password": "password123"})

    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data, "Expected 'id' in response"
    assert "username" in data, "Expected 'username' in response"
    assert data["username"] == username, "Registered username does not match"


def test_login_user():
    """
    Test user login and JWT token generation.
    """
    username = generate_random_user()
    client.post("/register", json={"username": username, "password": "password123"})  # Register first
    
    response = client.post("/", json={"username": username, "password": "password123"})
    
    assert response.status_code == 200
    assert "access_token" in response.cookies, "JWT token not found in cookies"
