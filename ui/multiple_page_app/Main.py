import streamlit as st

from api.api import get_all_items, register_user, get_jwt_token, add_item_to_favorite_items, get_favorite_items, \
    get_favorite_items_by_user_id, delete_favorite_item, create_order, get_order_by_user_id, close_order, \
    delete_item_from_order, get_temp_order

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
        'get_order_by_user_id': get_order_by_user_id,
        'get_temp_order': get_temp_order,
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


st.set_page_config(
    page_title="Speakers Web-Shop🎧",
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
st.title("Speakers Web-Shop")
st.header("All Items in Stock")

# Fetch all items from the database
try:
    items = get_all_items()
except Exception as e:
    st.error(f"Error fetching items: {e}")
    items = []

if items:
    row1 = st.columns(4)
    row2 = st.columns(4)

    grid = [col.container(height=200) for col in row1 + row2]

    for i, item in enumerate(items[:len(grid)]):
        with grid[i]:
            st.markdown(f"**{item['name']}**")
            st.markdown(f"*Price: ${item['price']}*")
            st.markdown(f"Item Stock: {item['item_stock']}")
            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("Add to order", key=f"order_{i}"):
                    if 'jwt_token' in st.session_state and st.session_state['jwt_token']:
                        user_id = st.session_state.get("user_id")
                        try:
                            temp_order_response = get_temp_order(user_id)
                            if temp_order_response.get("success"):
                                temp_order = temp_order_response.get("data")
                                order_id = temp_order["id"]

                                st.session_state.current_order_id = order_id
                                if 'order_quantities' not in st.session_state:
                                    st.session_state.order_quantities = {}
                                order_quantities = st.session_state.order_quantities
                                if item["id"] in st.session_state.order_quantities:
                                    st.session_state.order_quantities[item["id"]] += 1
                                else:
                                    st.session_state.order_quantities[item["id"]] = 1
                                add_order_response = add_item_to_order(user_id, item["id"], 1)
                                st.success(f"'{item['name']}' Added to your existing order!")

                            else:
                                shipping_address = st.session_state.get("user_address", "Default Address")
                                item_quantities = {item["id"]: 1}
                                item_price = item["price"]
                                total_price = item_price * item_quantities[item["id"]]
                                new_order = create_order(user_id, shipping_address, item_quantities, total_price, 'TEMP')

                                st.session_state.current_order_id = new_order["id"]
                                st.session_state.order_quantities = item_quantities
                            st.success(f"{item['name']} added to your order!")

                        except Exception as e:
                            st.error(f"Error processing order: {e}")
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


#     num_columns = 3  # Number of columns in the grid
#     for row in range(0, len(items), num_columns):
#         row_items = items[row: row + num_columns]
#         cols = st.columns(num_columns)
#
#         for listing, item in enumerate(row_items):
#             with cols[listing]:
#                 st.markdown(
#                     f"""
#                     <div class="item-frame">
#                         <h3>{item['name']}</h3>
#                         <p><b>Price:</b> ${item['price']:.2f}</p>
#                         <p><b>Stock:</b> {item['item_stock']}</p>
#                         <button style="background-color: #007BFF; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer;">
#                             Add to Cart
#                         </button>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
# else:
#     st.info("No items found in the database.")
#
# # Close the page frame div
# st.markdown("</div>", unsafe_allow_html=True)
