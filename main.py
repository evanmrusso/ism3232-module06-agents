# main.py
# Author: Evan Russo

from change_queue import ChangeQueue
from chatbot import SupportChatbot
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from ollama_model import OllamaModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """you are Sunny, a support assistant for Bayside Outfitters.
Answer in one short sentence.
Store hours are 10 am to 7 pm every day.
Returns are accepted within 30 days with a receipt.
Shipping takes 3 to 5 business days.
Sale items cannot be returned.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to a human agent."""

ORDERS = {
    "A100": {"status": "shipped", "address": "14 Bay Road."},
    "A101": {"status": "processing", "address": "3 Gull Lane."},
    "A102": {"status": "delivered", "address": "88 Pier Street."},
}

STOCK = {
    "rain jacket": 12,
    "day pack": 0,
    "trail hat": 5,
}


order_tool = OrderLookup(ORDERS)
stock_tool = StockLookup(STOCK)
change_queue = ChangeQueue(order_tool)
model = FallbackModel(OllamaModel(MODEL_NAME), KeywordModel())
tools = Toolbox(order_tool, stock_tool, change_queue)
bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in change_queue.waiting():
    number = request["number"]
    print(f"Order {number}: {request['order_id']} to {request['new_address']}")
    answer = input("Approve? (yes/no): ")
    if answer == "yes":
        print(change_queue.approve(number))
    else:
        print(change_queue.reject(number))

for order_id in ORDERS:
    print(order_id, ORDERS[order_id]["address"])
