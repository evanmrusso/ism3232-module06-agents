# my_assistant.py
# Author: Evan Russo

HANDOFF_WORDS = ["refund", "damage", "broke", "my order"]


class FAQAssistant:
    """A FAQ assistant for Grass Dragon. Rules handle the store information and handoffs. A model handles the rest."""

    # Claude helped: indented every method one level so it belongs to the class.
    def __init__(self, name, instructions, store_information, model):
        """Set up one assistant with its own name, instructions, tool, model, and  history."""
        self.name = name
        self.instructions = instructions
        self.store_information = store_information
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with refunds, damaged items, or orders here. I'm passing you to a store employee."
        if "?" in text:
            return self.faq_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has no answer."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "The model can't answer that right now. Try again in a few minutes."
        return reply

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
            return self.model_reply()
        answer = self.store_information.answer_for(keyword)
        return answer
