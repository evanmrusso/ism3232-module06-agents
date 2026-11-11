# my_toolbox.py
# Author: Evan Russo


class StoreToolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, store_information, hold_queue):
        """Hold the tools the model is allowed to ask for."""
        self.store_information = store_information
        self.hold_queue = hold_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.store_information.look_up_store_info,
            self.hold_queue.request_hold,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "look_up_store_info":
            topic = self.clean(arguments, "topic")
            if topic == "":
                return "The topic is missing. Ask the customer what they want to know."
            return self.store_information.look_up_store_info(topic)
        if name == "request_hold":
            item = self.clean(arguments, "item")
            customer = self.clean(arguments, "customer")
            if item == "" or customer == "":
                return "The item and the customer full name are both needed."
            if not self.customer_said(history, item):
                return "The customer has not named that item. Ask them for it."
            if not self.customer_said(history, customer):
                return "The customer has not given that name. Ask them for it."
            return self.hold_queue.request_hold(item, customer)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if the text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
