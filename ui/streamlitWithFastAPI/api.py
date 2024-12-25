import requests


BASE_URL = "http://localhost:8000"


def register_user(first_name, last_name, email, phone, address, username, password):
    url = f"{BASE_URL}/user/"
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address": address,
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response


def get_jwt_token(username, password):
    url = f"{BASE_URL}/auth/token"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=form_data)
    return response.json().get("jwt_token")


def get_all_users(token):
    url = f"{BASE_URL}/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()
