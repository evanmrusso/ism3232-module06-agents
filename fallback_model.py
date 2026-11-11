# fallback_model.py
# Author: Evan Russo


class FallbackModel:
    """Ask the first model. If it has no answer, ask the second."""

    def __init__(self, first, second):
        """Store the two models, in the order they are asked."""
        self.first = first
        self.second = second

    def decide(self, instructions, history, tools):
        """Return the first model's decision, or the second's if the first has none."""
        decision = self.first.decide(instructions, history, tools)
        if decision is None:
            decision = self.second.decide(instructions, history, tools)
        return decision
