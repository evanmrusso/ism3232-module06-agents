# my_assistant.py
# Author: Evan Russo

HANDOFF_WORDS = ["refund", "damage", "broke", "my order"]


class FAQAssistant:
    """A mock FAQ assistant for Grass Dragon, with replies from simple rules, not AI."""

    # Claude helped: indented every method one level so it belongs to the class.
    def __init__(self, name, instructions, store_information):
        """Set up one assistant with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.store_information = store_information
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with refunds, damaged items, or orders here. I'm passing you to a store employee."
        if "?" in text:
            return self.faq_reply(user_message)
        if "hello" in text:
            return f"Hello! I'm {self.name}. Ask me about our hours, locations, returns, shipping, or payment."
        return "I'm not sure how to help with that. I can answer questions about hours, locations, returns, shipping, and payment."

    def needs_human(self, text):
        """Return True if the message is about a refund, a damaged item, or an order, which a store employee must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def faq_reply(self, user_message):
        """Use store information to answer a question about faq information."""
        keyword = self.store_information.find_keyword(user_message)
        if keyword is None:
            return "Sorry, I don't have an answer for that. I can help with hours, locations, returns, shipping, and payment."
        answer = self.store_information.answer_for(keyword)
        return answer
