import streamlit as st

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
    print(response)
    return response


def get_jwt_token(username, password):
    url = f"{BASE_URL}/auth/token"
    form_data = {
        "username": username,
        "password": password
    }
    # print("form_data sent to /auth/token:", form_data)
    response = requests.post(url, data=form_data)
    # print("Login Response:", response.status_code, response.text)
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
            queries = [query.strip().lower() for query in name.split(",")]
            filtered_items = []
            for item in items:
                if any(query in item['name'].lower() for query in queries):
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


@st.cache_resource(ttl=10)
def get_all_users(token):
    url = f"{BASE_URL}/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


# @st.cache_resource(ttl=60)
# def get_user(user_id):
#     url = f"{BASE_URL}/user/{user_id}"
#     response = requests.get(url)
#     return response.json()

@st.cache_resource(ttl=60)
def get_user(user_id, token):
    url = f"{BASE_URL}/user/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


# def delete_user_by_id(user_id):
#     url = f"{BASE_URL}/user/{user_id}"
#     response = requests.delete(url)
#     response.raise_for_status()


@st.cache_resource(ttl=10)
def get_all_items():
    url = f"{BASE_URL}/item/"
    response = requests.get(url)
    return response.json()


def add_item_to_favorite_items(user_id, item_id):
    url = f"{BASE_URL}/favorite_item/"
    payload = {"user_id": user_id, "item_id": item_id}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
    # except requests.exceptions.HTTPError as http_err:
    #     return {"error": f"HTTP error occurred: {http_err}"}
    # except Exception as err:
    #     return {"error": f"An error occurred: {err}"}


# @st.cache_resource(ttl=10)
def get_favorite_items_by_user_id(user_id):
    url = f"{BASE_URL}/favorite_item/user/{user_id}"
    response = requests.get(url)
    return response.json()


@st.cache_resource(ttl=10)
def get_favorite_items():
    url = f"{BASE_URL}/favorite_item/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def delete_favorite_item(user_id, item_id):
    url = f"{BASE_URL}/favorite_item/{user_id}/item/{item_id}"
    response = requests.delete(url)
    response.raise_for_status()


def create_order(user_id, shipping_address, item_quantities, total_price, status="TEMP"):
    url = f"{BASE_URL}/order/"
    payload = {
        "user_id": user_id,
        "shipping_address": shipping_address,
        "item_quantities": item_quantities,
        "total_price": total_price,
        "status": status
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def update_temp_order_quantities(user_id, item_id, quantity):
    url = f"{BASE_URL}/order//update_order_quantities"
    payload = {
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity
    }
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()


def close_order(order_id, shipping_address, user_id):
    url = f"{BASE_URL}/order/purchase/{order_id}"
    payload = {
        "order_id": order_id,
        "user_id": user_id,
        "shipping_address": shipping_address,
        "status": "CLOSE",
    }
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()


# @st.cache_resource(ttl=10)
# def get_order_by_user_id(user_id):
#     url = f"{BASE_URL}/order/user/{user_id}"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

@st.cache_resource(ttl=10)
def get_order_by_id(order_id):
    url = f"{BASE_URL}/order/{order_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@st.cache_resource(ttl=10)
def get_order_by_order_and_user_id(order_id, user_id):
    url = f"{BASE_URL}/order/{order_id}/user/{user_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@st.cache_resource(ttl=1)
def get_temp_order(user_id):
    url = f"{BASE_URL}/order/temp/{user_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def delete_order(order_id):
    url = f"{BASE_URL}/order/{order_id}"
    response = requests.delete(url)
    response.raise_for_status()


def delete_item_from_order(order_id, item_id):
    url = f"{BASE_URL}/order/{order_id}/item/{item_id}"
    response = requests.delete(url)
    response.raise_for_status()
