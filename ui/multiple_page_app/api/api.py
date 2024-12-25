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

    # response = requests.post(url, json=payload)
    # response.raise_for_status()
    # response_data = response.json()
    # jwt_token = response_data.get("jwt_token")
    # user_id = response_data.get("user_id")
    # return jwt_token, user_id
    # try:
    #     response = requests.post(url, json=payload)
    #     if response.status_code == 201:
    #         return response.json()  # Expecting a JSON response on success
    #     elif response.status_code == 400:
    #         print("Validation error:", response.text)
    #         return None
    #     else:
    #         print("Unexpected status code:", response.status_code)
    #         return None
    # except Exception as e:
    #     print(f"Error during registration: {e}")
    #     return None


# def get_jwt_token(username, password):
#     url = f"{BASE_URL}/auth/token"
#     form_data = {
#         "username": username,
#         "password": password
#     }
#     try:
#         response = requests.post(url, data=form_data)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         if response.headers.get('Content-Type') == 'application/json':
#             response_data = response.json()
#             jwt_token = response_data.get("jwt_token")
#             user_id = response_data.get("user_id")
#             return jwt_token, user_id
#         else:
#             print(f"Unexpected response content type: {response.text}")
#             return None, None
#     except requests.exceptions.RequestException as e:
#         print(f"Error during login: {e}")
#         return None, None

def get_jwt_token(username, password):
    url = f"{BASE_URL}/auth/token"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=form_data)
    response.raise_for_status()
    response_data = response.json()
    jwt_token = response_data.get("jwt_token")
    user_id = response_data.get("user_id")
    return jwt_token, user_id


def get_all_users(token):
    url = f"{BASE_URL}/user/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def get_all_items():
    url = f"{BASE_URL}/item/"
    response = requests.get(url)
    return response.json()


def add_item_to_favorite_items(user_id, item_id):
    url = f"{BASE_URL}/favorite_item/"
    payload = {"user_id": user_id, "item_id": item_id}
    print(f"Payload being sent: {payload}")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}


def get_favorite_items_by_user_id(user_id):
    url = f"{BASE_URL}/favorite_item/user/{user_id}"
    response = requests.get(url)
    print(response.json())
    return response.json()


def get_favorite_items():
    url = f"{BASE_URL}/favorite_item/"
    response = requests.get(url)
    return response.json()


def delete_favorite_item(item_id):
    url = f"{BASE_URL}/favorite_item/item/{item_id}"
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
    # print(f"Payload being sent: {payload}")
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def add_item_to_order(user_id, item_id, quantity):
    url = f"{BASE_URL}/order/add_to_order"
    payload = {
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity
    }
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()


def close_order(order_id):
    url = f"{BASE_URL}/order/{order_id}/purchase"
    response = requests.put(url)
    response.raise_for_status()
    return response.json()


def get_order_by_user_id(user_id):
    url = f"{BASE_URL}/order/user/{user_id}"
    response = requests.get(url)
    response.raise_for_status()
    print(f"get order{response.json()}")
    return response.json()


def get_temp_order(user_id):
    url = f"{BASE_URL}/order/temp/{user_id}"
    response = requests.get(url)
    response.raise_for_status()
    print(f"get order{response.json()}")
    return response.json()


def delete_item_from_order(order_id, item_id):
    url = f"{BASE_URL}/order/{order_id}/item/{item_id}"
    response = requests.delete(url)
    response.raise_for_status()


def delete_order(order_id):
    url = f"{BASE_URL}/order/{order_id}"
    response = requests.delete(url)
    response.raise_for_status()





