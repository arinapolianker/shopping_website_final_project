import streamlit as st

import requests

BASE_URL = "http://localhost:8000"


def register_user(first_name, last_name, email, phone, address, country, city, username, password):
    url = f"{BASE_URL}/user/"
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address": address,
        "country": country,
        "city": city,
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
    if response.status_code == 401:
        return None, None
    else:
        response.raise_for_status()
        response_data = response.json()
        jwt_token = response_data.get("jwt_token")
        user_id = response_data.get("user_id")
        return jwt_token, user_id


def fetch_filtered_items(name=None, stock_filter=None, price_filter=None):
    try:
        items = get_all_items()
        if name:
            search_terms = []
            special_commands = []

            for term in name.split(","):
                term = term.strip()
                parts = term.split()
                if len(parts) == 3 and parts[0] in ["stock", "price"] and parts[1] in ["<", ">", "="]:
                    special_commands.append(parts)
                else:
                    search_terms.append(term.lower())
            if search_terms:
                filtered_items = []
                for item in items:
                    if any(term in item['name'].lower() for term in search_terms):
                        filtered_items.append(item)
                items = filtered_items

        if stock_filter:
            operator, value = stock_filter
            value = int(value)
            if operator == ">":
                items = [item for item in items if item['item_stock'] > value]
            elif operator == "<":
                items = [item for item in items if item['item_stock'] < value]
            elif operator == "=":
                items = [item for item in items if item['item_stock'] == value]
        if price_filter:
            operator, value = price_filter
            value = float(value)
            if operator == ">":
                items = [item for item in items if item['price'] > value]
            elif operator == "<":
                items = [item for item in items if item['price'] < value]
            elif operator == "=":
                items = [item for item in items if item['price'] == value]
        return items
    except Exception as e:
        st.error(f"Error fetching items: {e}")
        return []


def get_user(user_id, token):
    url = f"{BASE_URL}/user/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def logout_user(token):
    url = f"{BASE_URL}/user/logout/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(url, headers=headers)
    return response.json()


def delete_user_by_id(user_id, token):
    url = f"{BASE_URL}/user/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


@st.cache_resource(ttl=30)
def get_all_items():
    url = f"{BASE_URL}/item/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def add_item_to_favorite_items(user_id, item_id, token):
    url = f"{BASE_URL}/favorite_item/"
    payload = {"user_id": user_id, "item_id": item_id}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def get_favorite_items_by_user_id(user_id, token):
    url = f"{BASE_URL}/favorite_item/user/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def delete_favorite_item(user_id, item_id, token):
    url = f"{BASE_URL}/favorite_item/{user_id}/item/{item_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def create_order(user_id, token, shipping_address, item_quantities, total_price, status="TEMP"):
    url = f"{BASE_URL}/order/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "user_id": user_id,
        "shipping_address": shipping_address,
        "item_quantities": item_quantities,
        "total_price": total_price,
        "status": status
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def update_temp_order_quantities(user_id, item_id, quantity, token):
    url = f"{BASE_URL}/order/update_order_quantities/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity
    }
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def close_order(order_id, shipping_address, user_id, token):
    url = f"{BASE_URL}/order/purchase/{order_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "order_id": order_id,
        "user_id": user_id,
        "shipping_address": shipping_address,
        "status": "CLOSE",
    }
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


@st.cache_resource(ttl=30)
def get_order_by_user_id(user_id, token):
    url = f"{BASE_URL}/order/user/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_order_by_id(order_id):
    url = f"{BASE_URL}/order/{order_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# @st.cache_resource(ttl=2)
def get_temp_order(user_id, token):
    url = f"{BASE_URL}/order/temp/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def delete_item_from_order(order_id, item_id, token):
    url = f"{BASE_URL}/order/{order_id}/item/{item_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
