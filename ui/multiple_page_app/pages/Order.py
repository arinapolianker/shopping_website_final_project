import streamlit as st

get_jwt_token = st.session_state.functions['get_jwt_token']
user_id = st.session_state.get('user_id')

get_order_by_user_id = st.session_state.functions['get_order_by_user_id']
create_order = st.session_state.functions['create_order']
close_order = st.session_state.functions['close_order']
delete_item_from_order = st.session_state.functions['delete_item_from_order']

if "jwt_token" not in st.session_state or not st.session_state.jwt_token:
    st.warning("You must be logged in to view this page.")
    st.stop()

st.set_page_config(
    page_title="Order 🛒",  # Sets the browser tab title
    page_icon="🛒",  # Optional: Add a shopping cart emoji as an icon
    layout="wide",  # Optional: Choose layout
)

st.title("Order 🛒")

try:
    order = get_order_by_user_id(user_id)
    if order and order['status'] == 'TEMP':
        st.session_state.current_order_id = order['id']
        st.session_state.order_quantities = order['item_quantities']
    else:
        st.info("You have no active orders.")
except Exception as e:
    st.error(f"Error fetching items: {e}")
    order = None

if order:
    st.markdown("### Order Summary")
    total_price = 0.0

    with st.form("order_summary"):
        # item_quantities = {}
        for item_id, quantity in st.session_state.order_quantities.items():
            item_details = get_order_by_user_id(user_id)
            # item = order['']
            # item_detail = next((item for item in items if item["id"] == item_id), None)
            if item_details:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{item_details['name']}**")
                with col2:
                    new_quantity = st.number_input(
                        f"Quantity for {item_details['name']}", min_value=1, value=quantity
                    )
                    st.session_state.order_quantities[item_id] = new_quantity
                with col3:
                    st.markdown(f"${item_details['price'] * new_quantity:.2f}")
                with col4:
                    if st.button(f"Remove {item_details['name']}", key=f"remove_{item_id}"):
                        del st.session_state.order_quantities[item_id]
                        delete_item_from_order(order['id'], item_id)
                        st.success(f"{item_details['name']} removed from your order!")
                total_price += item_details['price'] * new_quantity

        st.markdown(f"### Total Price: ${total_price:.2f}")
        shipping_address = st.text_input("Shipping Address", value=order['shipping_address'])

    if st.form_submit_button("Place Order"):
        if shipping_address:
            try:
                # user_id = st.session_state.get("user_id")
                close_order(order['id'])
                st.success("Your order has been placed!")
                st.session_state.order_quantities.clear()
            except Exception as e:
                st.error(f"Error finalizing order: {e}")
        else:
            st.warning("Please provide a shipping address.")
else:
    st.info("Your order is currently empty.")
