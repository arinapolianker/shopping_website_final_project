import random

import streamlit as st

get_jwt_token = st.session_state.functions['get_jwt_token']
user_id = st.session_state.get('user_id')

get_order_by_user_id = st.session_state.functions['get_order_by_user_id']
get_temp_order = st.session_state.functions['get_temp_order']
get_order_by_order_and_user_id = st.session_state.functions['get_order_by_order_and_user_id']
update_temp_order_quantities = st.session_state.functions['update_temp_order_quantities']
close_order = st.session_state.functions['close_order']
delete_item_from_order = st.session_state.functions['delete_item_from_order']

if "jwt_token" not in st.session_state or not st.session_state.jwt_token:
    st.warning("You must be logged in to view this page.")
    st.stop()

if 'order_quantities' not in st.session_state:
    st.session_state['order_quantities'] = {}

if 'temp_order' not in st.session_state:
    st.session_state['temp_order'] = None

if 'order_summary' not in st.session_state:
    st.session_state['order_summary'] = None

st.set_page_config(
    page_title="Order",
    page_icon="🛒",
    layout="wide",
)

st.title("Order 🛒")
# if not st.session_state.order_summary:
try:
    temp_order = get_temp_order(user_id)
    if temp_order:
        st.session_state.temp_order = temp_order
        st.session_state.current_order_id = temp_order['id']
        st.session_state.order_quantities = temp_order['item_quantities']
        st.session_state.total_price = temp_order['total_price']
except Exception as e:
    st.error(f"Error fetching items: {e}")
    temp_order = None

if st.session_state.order_summary:
    order_summary = st.session_state.order_summary

    st.success("Your order has been placed! 🎉")
    st.markdown("### Order Summary")
    for item in order_summary['item']:
        st.markdown(f"- **{item['name']}**: {item['quantity']} x ${item['price']:.2f}")
    st.markdown(f"**Total Price:** ${order_summary['total_price']:.2f}")
    st.markdown(f"**Shipping Address:** {order_summary['shipping_address']}")
    st.markdown(f"**Order Number:** {order_summary['order_number']}")
    st.markdown(f"**Order Date:** {order_summary['order_date']}")

elif st.session_state.temp_order:
    temp_order = st.session_state.temp_order
    st.markdown("### Order Summary")
    total_price = 0.0

    for item in temp_order['item']:
        item_id = item['id']
        quantity = st.session_state.order_quantities.get(str(item_id), item['quantity'])

        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            quantity_key = f"quantity_{item_id}"
            new_quantity = st.number_input(
                f"Quantity for {item['name']}",
                min_value=0,
                value=quantity,
                key=quantity_key
            )
            if new_quantity != quantity and new_quantity != 0:
                update_temp_order_quantities(user_id, item_id, new_quantity)
                st.session_state.order_quantities[item_id] = new_quantity
                st.rerun()
            if new_quantity == 0:
                update_temp_order_quantities(user_id, item_id, 0)
                updated_temp_order = get_temp_order(user_id)
                st.session_state.temp_order = updated_temp_order
                st.session_state.order_quantities = updated_temp_order['item_quantities']
                st.success(f"{item['name']} removed from your order!")
                st.rerun()
        with col3:
            item_total_price = item['price'] * new_quantity
            total_price += item_total_price
            st.markdown(f"${item_total_price:.2f}")
        with col4:
            if st.checkbox(f"Remove {item['name']}", key=f"remove_{item_id}"):
                update_temp_order_quantities(user_id, item_id, 0)
                updated_temp_order = get_temp_order(user_id)
                st.session_state.temp_order = updated_temp_order
                st.session_state.order_quantities = updated_temp_order['item_quantities']
                st.success(f"{item['name']} removed from your order!")
                st.rerun()

    st.session_state.total_price = total_price
    st.markdown(f"### Total Price: ${st.session_state.total_price:.2f}")
    shipping_address = st.text_input("Shipping Address", value=temp_order['shipping_address'])

    if st.button("Place Order"):
        if shipping_address:
            order_number = random.randint(10000, 99999)
            close_order(temp_order['id'], shipping_address, user_id)

            st.success(f"Your order has been placed! 🎉")
            st.write(f"### Order Summary:")

            finished_order = get_order_by_order_and_user_id(temp_order['id'], user_id)
            print(f"finished order: {finished_order}")
            st.session_state.order_summary = {
                "item": finished_order['item'],
                "total_price": st.session_state.total_price,
                "shipping_address": shipping_address,
                "order_date": finished_order['order_date'],
                "order_number": order_number,
            }
            st.session_state.temp_order = None
            st.session_state.order_quantities = {}
            st.session_state.total_price = 0.0

            st.rerun()
        else:
            st.warning("Please provide a shipping address.")
else:
    st.info("Your order is currently empty.")

# st.rerun()
