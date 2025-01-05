import streamlit as st

from api.api import get_all_items, register_user, get_jwt_token, add_item_to_favorite_items, get_favorite_items, \
    get_favorite_items_by_user_id, delete_favorite_item, create_order, get_order_by_user_id, close_order, \
    delete_item_from_order, get_temp_order, update_temp_order_quantities, get_order_by_order_and_user_id, \
    fetch_filtered_items

if 'functions' not in st.session_state:
    st.session_state.functions = {
        'register_user': register_user,
        'get_jwt_token': get_jwt_token,
        'get_all_items': get_all_items,
        'add_item_to_favorite_items': add_item_to_favorite_items,
        'get_favorite_items': get_favorite_items,
        'get_favorite_items_by_user_id': get_favorite_items_by_user_id,
        'delete_favorite_item': delete_favorite_item,
        'create_order': create_order,
        'update_temp_order_quantities': update_temp_order_quantities,
        'get_order_by_user_id': get_order_by_user_id,
        'get_temp_order': get_temp_order,
        'get_order_by_order_and_user_id': get_order_by_order_and_user_id,
        'close_order': close_order,
        'delete_item_from_order': delete_item_from_order
    }

if 'jwt_token' not in st.session_state:
    st.session_state.jwt_token = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'order_quantities' not in st.session_state:
    st.session_state.order_quantities = {}
# if 'current_order_id' not in st.session_state:
#     st.session_state.current_order_id = None

# page_names = {
#     "Chat_Assistant.py": "Chat Assistant",
#     "Favorites.py": "Favorites",
#     "orders.py": "Orders",
#     "Account.py": "Account",  # Includes login, logout, and registration
#     "Home.py": "Home"
# }
#
# selected_page = st.sidebar.radio("Navigate", list(page_names.values()))
# for file, name in page_names.items():
#     if name == selected_page:
#         page_module = import_module(f"pages.{file.replace('.py', '')}")
#         page_module.run()  # Each page script should have a `run()` function
#         break

st.set_page_config(
    page_title="Speakers Web-Shop",
    page_icon="🎧",
    layout="wide",
)

st.title("Welcome to the Speakers Web-Shop!")

# st.markdown(
#     """
#     <style>
#         .page-frame {
#             background-color: #f9f9f9;
#             border: 2px solid #007BFF;
#             border-radius: 20px;
#             padding: 20px;
#         }
#         .item-frame {
#             background-color: #ffffff;
#             border: 1px solid #d3d3d3;
#             border-radius: 10px;
#             padding: 15px;
#             margin-bottom: 20px;
#             text-align: center;
#         }
#         .item-frame:hover {
#             border-color: #007BFF;
#             box-shadow: 0px 4px 6px rgba(0, 123, 255, 0.2);
#         }
#         .grid-row {
#             display: flex;
#             justify-content: space-between;
#         }
#         .grid-column {
#             flex: 1;
#             margin: 0 10px;
#         }
#         body {
#             background-color: #e9ecef;
#         }
#     </style>
#     <div class="page-frame">
#     """,
#     unsafe_allow_html=True,
# )
# Streamlit headline

try:
    items = get_all_items()
except Exception as e:
    st.error(f"Error fetching items: {e}")
    items = []

# st.header("Search and Filter Items")
search_by_name = st.text_input("Search by Name (use commas for multiple words)")
price_filter = st.slider("Filter by Price", 0, 500, (0, 500))  # Range slider
stock_filter = st.slider("Filter by Stock", 0, 100, (0, 100))  # Range slider

name_keywords = [keyword.strip().lower() for keyword in search_by_name.split(",") if keyword.strip()]
filtered_items = [
    item for item in items
    if (not name_keywords or any(keyword in item["name"].lower() for keyword in name_keywords))
    and price_filter[0] <= item["price"] <= price_filter[1]
    and stock_filter[0] <= item["item_stock"] <= stock_filter[1]
]

if filtered_items:
    st.markdown("### Available Items")
    # row1 = st.columns(4)
    # row2 = st.columns(4)
    # rows = []
    #
    # grid = [col.container(height=200) for col in row1 + row2]
    num_columns = 4
    rows = [st.columns(num_columns) for _ in range((len(items) + num_columns - 1) // num_columns)]

    for i, item in enumerate(filtered_items):
        row_idx = i // num_columns
        col_idx = i % num_columns
        # for i, item in enumerate(items[:len(grid)]):
        with rows[row_idx][col_idx]:
            st.markdown(f"**{item['name']}**")
            st.markdown(f"*Price: ${item['price']}*")
            st.markdown(f"Item Stock: {item['item_stock']}")
            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("Add to order", key=f"order_{i}"):
                    if 'jwt_token' in st.session_state and st.session_state['jwt_token']:
                        user_id = st.session_state.get("user_id")
                        temp_order = get_temp_order(user_id)
                        if not temp_order:
                            shipping_address = st.session_state.get("user_address", "Default Address")
                            item_quantities = {item["id"]: 1}
                            item_price = item["price"]
                            total_price = item_price * item_quantities[item["id"]]
                            create_order(user_id, shipping_address, item_quantities, total_price, 'TEMP')
                            st.session_state.order_quantities = item_quantities
                            st.success(f"{item['name']} added to your order!")

                        else:
                            item_quantities = temp_order.get("item_quantities", {})
                            item_id_str = str(item['id'])
                            current_quantity = item_quantities.get(item_id_str, 0)
                            new_quantity = current_quantity + 1
                            update_temp_order_quantities(user_id, item['id'], new_quantity)
                            st.session_state.order_quantities[item['id']] = new_quantity
                            st.success(f"'{item['name']}' Added to your existing order!")
                    else:
                        st.warning("Please log in to add items to your order.")

            with col2:
                if st.button("Add to favorite items list", key=f"favorite_{i}"):
                    if 'jwt_token' in st.session_state and st.session_state['jwt_token']:
                        user_id = st.session_state.get("user_id")
                        favorite_items = get_favorite_items_by_user_id(user_id)

                        if any(favorite_item['item']['id'] == item['id'] for favorite_item in favorite_items):
                            st.error(f"You already added '{item['name']}' to your favorite item list")
                        else:
                            response = add_item_to_favorite_items(user_id, item['id'])
                            st.success(f"{item['name']} was Added to favorite items!")
                            st.session_state["favorite_items_updated"] = True
                    else:
                        st.warning("Please log in to add items to your favorite list.")
else:
    st.warning("No items available.")
