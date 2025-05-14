import httpx
from config.config import Config
from controller import item_controller

config = Config()

HEADERS = {
    "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

user_conversations = {}


async def get_answer(question: str, user_id: int):
    try:
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        user_conversations[user_id].append({"role": "user", "content": question})
        items = await item_controller.get_all_items()
        store_context = (
                "You are a store assistant chatbot. You can answer questions about stock and prices "
                "using the provided product data. If a user wants to purchase an item, you should "
                "guide them to the Home page to add it to their cart if it's available in stock. "
                "Here is the store's product data:\n" +
                "\n".join([f"{item.name} has {item.item_stock} in stock, priced at {item.price}."
                           for item in items])
        )

        messages = [
            {"role": "system", "content": store_context},
            *user_conversations[user_id][-5:]
        ]

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(config.CHAT_GPT_API_URL,
                                         headers=HEADERS,
                                         json=payload)
            response.raise_for_status()
            assistant_response = response.json()['choices'][0]['message']['content']

        user_conversations[user_id].append({"role": "assistant", "content": assistant_response})
        return assistant_response

    except httpx.ConnectTimeout:
        error_message = "Sorry, I'm having trouble connecting to my knowledge service. Please try again in a moment."
        user_conversations[user_id].append({"role": "assistant", "content": error_message})
        return error_message

    except httpx.HTTPStatusError as e:
        error_message = f"Sorry, there was an issue with the request: {e.response.status_code}"
        user_conversations[user_id].append({"role": "assistant", "content": error_message})
        return error_message

