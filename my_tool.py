# my_tools.py
# Author: Evan Russo


class StoreInformation:
    """Stores the Grass Dragon FAQ answers for holiday hours, store hours, locations, returns, shipping, and payment. It knows nothing about customer orders and nothing about chatting with a customer."""

    def __init__(self, faq_information):
        """Store the faq information this tool can look up"""
        self.faq_information = faq_information

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
