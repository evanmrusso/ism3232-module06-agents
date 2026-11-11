# my_tools.py
# Author: Evan Russo


class StoreInformation:
    """Stores the Grass Dragon FAQ answers for holiday hours, store hours, locations, returns, shipping, and payment. It knows nothing about customer orders and nothing about chatting with a customer."""

    def __init__(self, faq_information, products):
        """Store the faq answers and products this tool can look up. Start with no holds."""
        self.faq_information = faq_information
        self.products = products
        self.holds = []

    def find_keyword(self, text):
        """Return the first keyword mentioned in text, or None."""
        for keyword in self.faq_information:
            if keyword in text.lower():
                return keyword
        return None

    def answer_for(self, keyword):
        """Return the answer for keyword, or None if the keyword is unknown."""
        if keyword in self.faq_information:
            return self.faq_information[keyword]
        return None

    def find_product(self, text):
        """Return the first product mentioned in text, or None."""
        for product in self.products:
            if product in text.lower():
                return product
        return None

    def look_up_store_info(self, topic):
        """Look up store fact, Like hours, hoildays, locations,returns, shipping, or payment.

        Args:
            topic: What the customer asked about, like hours, holidays, locations, returns, shipping, or payment.
        """
        keyword = self.find_keyword(topic)
        if keyword is None:
            return "That topic was not found. I can check hours, holidays, locations, returns, shipping, or payment."
        return self.answer_for(keyword)

    def add_hold(self, item, customer):
        """Record one hold. Only an approval calls this."""
        self.holds.append({"item": item, "customer": customer})
