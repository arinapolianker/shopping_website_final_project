import time
import streamlit as st


get_jwt_token = st.session_state.functions['get_jwt_token']
get_favorite_items = st.session_state.functions['get_favorite_items']
get_favorite_items_by_user_id = st.session_state.functions['get_favorite_items_by_user_id']
delete_favorite_item = st.session_state.functions['delete_favorite_item']

get_temp_order = st.session_state.functions['get_temp_order']
create_order = st.session_state.functions['create_order']
update_temp_order_quantities = st.session_state.functions['update_temp_order_quantities']

user_id = st.session_state.get('user_id')

if "jwt_token" not in st.session_state or not st.session_state.jwt_token:
    st.warning("You must be logged in to view this page.")
    st.stop()

if 'favorite_items' not in st.session_state:
    st.session_state['favorite_items'] = None

# if "favorite_items" not in st.session_state:
#     st.session_state["favorite_items"] = get_favorite_items_by_user_id(user_id)

st.set_page_config(
    page_title="Favorite Items",
    page_icon="⭐",
    layout="wide",
)

st.title(" My Favorites❤️")

# if "success_message" in st.session_state:
#     st.success(st.session_state.success_message)
#     time.sleep(5)
#     del st.session_state.success_message
#     st.rerun()

try:
    favorite_items = get_favorite_items_by_user_id(user_id)
    if favorite_items:
        st.session_state.favorite_items = favorite_items
except Exception as e:
    st.error(f"Error fetching items: {e}")
    favorite_items = None


if favorite_items:
    cols = st.columns(3)
    for i, item in enumerate(favorite_items):
        item = item["item"]
        with cols[i % 3]:
            with st.container():
                st.markdown(f"### {item['name']}")
                st.markdown(f"**Price:** ${item['price']:.2f}")
                if item['item_stock'] > 0:
                    st.markdown(f"**Stock:** :green[{item['item_stock']} available]")
                else:
                    st.markdown(f"**Stock:** :red[Out of stock]")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🛒 Add to Cart", key=f"add_{i}", disabled=item['item_stock'] == 0):
                        temp_order = get_temp_order(user_id)
                        if not temp_order or "item" not in temp_order:
                            shipping_address = st.session_state.get("user_address", "Default Address")
                            item_quantities = {item["id"]: 1}
                            total_price = sum(item["price"] * quantity for item_id, quantity in item_quantities.items())
                            create_order(user_id, shipping_address, item_quantities, total_price, 'TEMP')
                            st.session_state.order_quantities = item_quantities
                            st.success(f"{item['name']} added to your order!")

                        else:
                            existing_item = {order_item["item_id"] for order_item in temp_order["item"]}
                            item_id = item["id"]
                            if item_id in existing_item:
                                item_quantities = {order_item["item_id"]: order_item["quantity"] for order_item in
                                                   temp_order["item"]}
                                current_quantity = item_quantities.get(item_id, 0)
                                new_quantity = current_quantity + 1
                                if new_quantity > item["item_stock"]:
                                    st.warning(
                                        f"Cannot add more '{item['name']}' to your order. Only {item['item_stock']} are available.")
                                else:
                                    update_temp_order_quantities(user_id, item_id, new_quantity)
                                    st.success(f"'{item['name']}' quantity updated in your order!")
                            else:
                                update_temp_order_quantities(user_id, item_id, 1)
                                st.success(f"'{item['name']}' added to your order!")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_{i}"):
                        delete_favorite_item(user_id, item["id"])
                        st.success(f"Removed '{item['name']}' from favorites.")
                        time.sleep(4)
                        st.rerun()
                st.markdown("---")
    # rows = st.columns(4)
    # grid = [col.container() for col in rows]
    #
    # for i, favorite in enumerate(favorite_items[:len(grid)]):
    #     item = favorite["item"]
    #     with grid[i]:
    #         st.markdown(f"**{item['name']}**")
    #         st.markdown(f"*Price: ${item['price']}*")
    #         st.markdown(f"Item Stock: {item['item_stock']}")
    #         col1, col2 = st.columns([1, 1])
    #         with col1:
    #             if st.button("Add to order", key=f"order_{i}"):
    #                 temp_order = get_temp_order(user_id)
    #                 if not temp_order or "item" not in temp_order:
    #                     shipping_address = st.session_state.get("user_address", "Default Address")
    #                     item_quantities = {item["id"]: 1}
    #                     total_price = sum(item["price"] * quantity for item_id, quantity in item_quantities.items())
    #                     create_order(user_id, shipping_address, item_quantities, total_price, 'TEMP')
    #                     st.session_state.order_quantities = item_quantities
    #                     st.success(f"{item['name']} added to your order!")
    #
    #                 else:
    #                     existing_item = {order_item["item_id"] for order_item in temp_order["item"]}
    #                     item_id = item["id"]
    #                     if item_id in existing_item:
    #                         item_quantities = {order_item["item_id"]: order_item["quantity"] for order_item in
    #                                            temp_order["item"]}
    #                         current_quantity = item_quantities.get(item_id, 0)
    #                         new_quantity = current_quantity + 1
    #                         # print(f"update sent to api from home: {user_id}, {item_id}, {new_quantity}")
    #                         update_temp_order_quantities(user_id, item_id, new_quantity)
    #                         # st.session_state.order_quantities[item['id']] = new_quantity
    #                         st.success(f"'{item['name']}' quantity updated in your order!")
    #                     else:
    #                         update_temp_order_quantities(user_id, item_id, 1)
    #                         st.success(f"'{item['name']}' added to your order!")
    #                 # if not temp_order:
    #                 #     shipping_address = st.session_state.get("user_address", "Default Address")
    #                 #     item_quantities = {item["id"]: 1}
    #                 #     item_price = item["price"]
    #                 #     total_price = item_price * item_quantities[item["id"]]
    #                 #     create_order(user_id, shipping_address, item_quantities, total_price, 'TEMP')
    #                 #     st.session_state.order_quantities = item_quantities
    #                 #     st.success(f"{item['name']} added to your order!")
    #                 #
    #                 # else:
    #                 #     item_quantities = temp_order.get("item_quantities", {})
    #                 #     item_id_str = str(item['id'])
    #                 #     current_quantity = item_quantities.get(item_id_str, 0)
    #                 #     new_quantity = current_quantity + 1
    #                 #     update_temp_order_quantities(user_id, item['id'], new_quantity)
    #                 #     st.session_state.order_quantities[item['id']] = new_quantity
    #                 #     st.success(f"'{item['name']}' Added to your existing order!")
    #         with col2:
    #             if st.button("Remove", key=f"remove_{i}"):
    #                 delete_favorite_item(user_id, item["id"])
    #                 st.success(f"Removed '{item['name']}' from favorites.")
    #                 time.sleep(4)
    #                 st.rerun()
else:
    st.info("You haven't added any items to your favorites yet")

