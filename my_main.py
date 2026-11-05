# my_main.py
# Author: Evan Russo

from my_assistant import FAQAssistant
from my_tool import StoreInformation
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

FAQ_INFORMATION = {
    "christmas": "Our store hours stay the same on holidays.",
    "thanksgiving": "Our store hours stay the same on holidays.",
    "holiday": "Our store hours stay the same on holidays.",
    "where": "We have 6 locations: Tampa, San Francisco, Freehold, Rochester, Boca Raton, and Miami.",
    "located": "We have 6 locations: Tampa, San Francisco, Freehold, Rochester, Boca Raton, and Miami.",
    "location": "We have 6 locations: Tampa, San Francisco, Freehold, Rochester, Boca Raton, and Miami.",
    "hours": "Our store hours are 9:00 am to 5:00 pm on weekdays and 12:00 pm to 4:00 pm on weekends.",
    "open": "Our store hours are 9:00 am to 5:00 pm on weekdays and 12:00 pm to 4:00 pm on weekends.",
    "close": "Our store hours are 9:00 am to 5:00 pm on weekdays and 12:00 pm to 4:00 pm on weekends.",
    "return": "Sorry, we don't accept returns on gear after it's purchased.",
    "exchange": "Sorry, we don't accept returns on gear after it's purchased.",
    "ship": "Online orders take 3-4 business days to ship.",
    "arrive": "Online orders take 3-4 business days to ship.",
    "deliver": "Online orders take 3-4 business days to ship.",
    "card": "We accept debit cards, credit cards, and cash.",
    "pay": "We accept debit cards, credit cards, and cash.",
    "cash": "We accept debit cards, credit cards, and cash.",
}

store_information = StoreInformation(FAQ_INFORMATION)
INSTRUCTIONS = """You are Kc, an assistant for Grass Dragon, a volleyball equipment store.
Answer in one short sentence.
We sell volleyballs, knee pads, and court shoes.
Teams of 6 or more players get 10 percent off.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to a store employee."""

model = OllamaModel(MODEL_NAME)
assistant = FAQAssistant(
    "Kc",
    INSTRUCTIONS,
    store_information,
    model,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
