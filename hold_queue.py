# hold_queue.py
# Author: Evan Russo


class HoldQueue:
    """Hold requests waiting for a store employee. Nothing is held until approved."""

    def __init__(self, store_information):
        """Start with no requests. Approved holds go into the store information."""
        self.store_information = store_information
        self.requests = []

    def request_hold(self, item, customer):
        """Ask a store employee to hold an item for pickup. An employee must approve it.

        Args:
            item: The product to hold, like knee pads.
            customer: The customer's full name.
        """
        found = self.store_information.find_product(item)
        if found is None:
            return "That item was not found. We carry volleyballs, knee pads, and court shoes."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "item": item,
            "customer": customer,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to a store employee. Nothing is on hold yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and record the hold."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.store_information.add_hold(request["item"], request["customer"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is held."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
