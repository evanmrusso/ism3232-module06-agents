from fake_model import FakeModel
from hold_queue import HoldQueue
from my_assistant import FAQAssistant
from my_tool import StoreInformation
from my_toolbox import StoreToolbox


class SilentModel:
    """A model that never has an answer. It stands in for ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_assistant(model):
    """Build a fresh assistant with its own tool for each test."""
    store = StoreInformation(
        {"hours": "We are open 9 to 5."}, ["volleyball", "knee pads"]
    )
    tools = StoreToolbox(store, HoldQueue(store))
    return FAQAssistant("Kc", "be precise", tools, model)


def hold(item, customer):
    """Build the decision a model returns when it wants to request a hold."""
    return {"tool": "request_hold", "arguments": {"item": item, "customer": customer}}


def test_model_can_look_up_store_info():
    model = FakeModel(
        [
            {"tool": "look_up_store_info", "arguments": {"topic": "hours"}},
            {"text": "We are open 9 to 5."},
        ]
    )
    assistant = make_assistant(model)
    assistant.respond("What are your hours?")
    assert assistant.history[1]["content"] == "We are open 9 to 5."


def test_hold_waits_for_a_store_employee():
    model = FakeModel([hold("knee pads", "Dana Cruz"), {"text": "sent."}])
    assistant = make_assistant(model)
    assistant.respond("Please hold knee pads for Dana Cruz")
    assert len(assistant.tools.hold_queue.waiting()) == 1
    assert assistant.tools.store_information.holds == []


def test_made_up_name_is_refused():
    model = FakeModel([hold("knee pads", "Jane Doe"), {"text": "Name?"}])
    assistant = make_assistant(model)
    assistant.respond("Please hold knee pads")
    assert "has not given that name" in assistant.history[1]["content"]
    assert assistant.tools.hold_queue.waiting() == []


def test_approval_records_the_hold_once():
    store = StoreInformation({}, ["knee pads"])
    queue = HoldQueue(store)
    queue.request_hold("knee pads", "Dana Cruz")
    queue.approve(1)
    queue.approve(1)
    assert len(store.holds) == 1


def test_unknown_tool_is_refused():
    model = FakeModel([{"tool": "delete_order", "arguments": {}}, {"text": "Sorry."}])
    assistant = make_assistant(model)
    assistant.respond("Delete my stuff.")
    assert assistant.history[1]["content"] == "There is no tool named delete_order."


def test_damaged_item_goes_to_a_person():
    assistant = make_assistant(FakeModel([]))
    assert "store employee" in assistant.respond("My knee pads broke.")


def test_unknown_request_gets_a_safe_reply():
    assistant = make_assistant(SilentModel())
    assert "try again" in assistant.respond("Tell me a joke")


def test_history_grows_by_two_each_turn():
    assistant = make_assistant(FakeModel([{"text": "Hi!"}, {"text": "Hello again!"}]))
    assistant.respond("hello")
    assistant.respond("hi.")
    assert len(assistant.history) == 4
