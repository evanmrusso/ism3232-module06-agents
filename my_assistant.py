# my_assistant.py
# Author: Evan Russo

from chatbot import MAX_TOOL_ROUNDS

HANDOFF_WORDS = ["refund", "damage", "broke", "my order"]


class FAQAssistant:
    """A FAQ assistant for Grass Dragon. Rules handle the store information and handoffs. A model handles the rest."""

    # Claude helped: indented every method one level so it belongs to the class.
    def __init__(self, name, instructions, tools, model):
        """Set up one assistant with its own name, instructions, tool, model, and  history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Pass refunds, damage, and orders to a person. Send the rest to the model."""
        if self.needs_human(user_message.lower()):
            return (
                "I can't help with refunds, damaged items, or orders here. "
                "I'm passing you to a store employee."
            )
        return self.model_reply()

    def needs_human(self, text):
        """Return True if the message is about a refund, a damaged item, or an order, which a store employee must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        rounds = 0
        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)
            if decision is None:
                return (
                    "Sorry, I can't answer that right now. try again in a few minutes."
                )
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "assistant",
                    "tool": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1
        return "Sorry, I couldn't finish that. I'm passing you to a store employee."
