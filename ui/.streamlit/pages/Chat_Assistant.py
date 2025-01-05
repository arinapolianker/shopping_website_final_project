import openai
import streamlit as st
from openai import OpenAI

# REMOVED = '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'

get_all_items = st.session_state.functions['get_all_items']

st.set_page_config(
    page_title="Chat Assistant 🤖",
    layout="wide",  # Optional: Choose layout (wide or centered)
    menu_items={
        'Get Help': None,  # Hide "Get Help" option
        'Report a bug': None,  # Hide "Report a bug" option
        'About': None,  # Hide "About" menu
    }
)

st.title("💬 Chatbot")
st.write("Welcome to the Chat Assistant page! Ask questions about the items in our store.")


with st.sidebar:
    if "REMOVED" not in st.session_state or not st.session_state.REMOVED:
        st.session_state.REMOVED = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        if st.session_state.REMOVED:
            st.success("API key saved!")
    else:
        st.text("Using saved OpenAI API Key")
        st.write("✔️ Your API key is already set.")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you?"}]
if "prompt_count" not in st.session_state:
    st.session_state["prompt_count"] = 0

items = get_all_items()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if st.session_state["prompt_count"] < 5 and (prompt := st.chat_input()):
    if "REMOVED" not in st.session_state or not st.session_state.REMOVED:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state["prompt_count"] += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # store_context = "Here is the store's product data:\n" + "\n".join(
    #     [f"{item['name']} (Stock: {item['item_stock']}): {item['price']}" for item in items]
    # )
    store_context = (
            "You are a store assistant chatbot. You can answer questions about stock and prices "
            "using the provided product data. Here is the store's product data:\n" +
            "\n".join([f"{item['name']} has {item['item_stock']} in stock, priced at {item['price']}."
                       for item in items])
    )
    context_messages = st.session_state.messages + [{"role": "system", "content": store_context}]

    client = OpenAI(api_key=st.session_state.REMOVED)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=context_messages)

    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=context_messages
    # )
    # msg = response['choices'][0]['message']['content']
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if st.session_state["prompt_count"] >= 5:
    st.warning("You have reached the maximum of 5 prompts for this session. Please refresh the page to restart.")
