import time
import streamlit as st

get_all_items = st.session_state.functions['get_all_items']
add_item_to_favorite_items = st.session_state.functions['add_item_to_favorite_items']
get_jwt_token = st.session_state.functions['get_jwt_token']
get_favorite_items = st.session_state.functions['get_favorite_items']
get_favorite_items_by_user_id = st.session_state.functions['get_favorite_items_by_user_id']
delete_favorite_item = st.session_state.functions['delete_favorite_item']
user_id = st.session_state.get('user_id')

if "jwt_token" not in st.session_state or not st.session_state.jwt_token:
    st.warning("You must be logged in to view this page.")
    st.stop()

st.set_page_config(
    page_title="Favorite Items⭐",  # Sets the browser tab title
    page_icon="⭐",  # Optional: Add a custom icon
    layout="wide",  # Optional: Choose layout
    menu_items={
        'Get Help': None,  # Hide "Get Help" option
        'Report a bug': None,  # Hide "Report a bug" option
        'About': None,  # Hide "About" menu
    }
)

st.title("Favorite Items")
st.write("Manage your favorite items here!")

try:
    # all_items = get_all_items()
    favorite_items = get_favorite_items_by_user_id(user_id)
except Exception as e:
    st.error(f"Error fetching items: {e}")
    # all_items = []
    favorite_items = []

# st.markdown(
#     """
#     <style>
#     .horizontal-scroll-container {
#         display: flex;
#         flex-direction: row;
#         overflow-x: auto;
#         gap: 20px;
#         padding: 10px;
#         white-space: nowrap;
#     }
#     .item-card {
#         flex: 0 0 auto;
#         width: 220px;
#         padding: 15px;
#         background-color: #f9f9f9;
#         border-radius: 10px;
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#         text-align: center;
#     }
#     .item-card:hover {
#         transform: scale(1.02);
#         transition: all 0.2s ease-in-out;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
#
# st.markdown('<div class="horizontal-scroll-container">', unsafe_allow_html=True)
#
# for item in all_items:
#     st.markdown(
#         f"""
#         <div class="item-card">
#             <h4>{item['name']}</h4>
#             <button onclick="window.location.reload()">Add to Favorites</button>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
# st.markdown('</div>', unsafe_allow_html=True)


# st.markdown("### Add Items to Favorites")
# if all_items:
#     container = st.container()
#     with container:
#         cols_per_row = 4
#         rows = [st.columns(cols_per_row) for _ in range((len(all_items) + cols_per_row - 1) // cols_per_row)]
#
#         for i, item in enumerate(all_items):
#             col = rows[i // cols_per_row][i % cols_per_row]
#             with col:
#                 st.markdown(f"**{item['name']}**")
#                 if st.button("Add to Favorites", key=f"add_{item['id']}"):
#                     add_item_to_favorite_items(item["name"])

    # for item in all_items:
    #     col1, col2 = st.columns([3, 1])
    #     with col1:
    #         st.markdown(f"**{item['name']}**")
    #     with col2:
    #         if st.button(f"Add {item['name']}", key=f"add_{item['id']}"):
    #             add_item_to_favorite_items(item["name"])
    #             st.session_state["favorite_items_updated"] = True
# else:
#     st.info("No items available.")

st.markdown("### Your Favorite Items")
if favorite_items:
    # row1 = st.columns(4)
    # row2 = st.columns(4)
    #
    # grid = [col.container(height=200) for col in row1 + row2]

    rows = st.columns(4)
    grid = [col.container() for col in rows]

    for i, favorite in enumerate(favorite_items[:len(grid)]):
        item = favorite["item"]
        with grid[i]:
            st.markdown(f"**{item['name']}**")
            st.markdown(f"*Price: ${item['price']}*")
            st.markdown(f"Item Stock: {item['item_stock']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.button("Add to order", key=f"order_{i}")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    delete_favorite_item(item["id"])
                    st.success(f"Removed '{item['name']}' from favorites.")
                    favorite_items = get_favorite_items()
                    # time.sleep(2)
                    # st.experimental_rerun()
                    # st.switch_page("FavoriteItems")
                    # st.session_state["favorite_items_updated"] = True
else:
    st.info("You have no favorite items.")

