from my_assistant import FAQAssistant
from my_tool import StoreInformation


def make_assistant():
    """Build a fresh assistant with its own tool for each test."""
    tool = StoreInformation(
        {
            "hours": "Our store hours are 9:00 am to 5:00 pm on weekdays and 12:00 pm to 4:00 pm on weekends.",
            "ship": "Online orders take 3-4 business days to ship.",
        }
    )
    return FAQAssistant("Kc", "be precise", tool)


def test_hours_question_uses_the_tool():
    assistant = make_assistant()
    reply = assistant.respond("What are your hours?")
    assert (
        reply
        == "Our store hours are 9:00 am to 5:00 pm on weekdays and 12:00 pm to 4:00 pm on weekends."
    )


def test_question_without_a_keyword_gets_a_helpful_reply():
    assistant = make_assistant()
    reply = assistant.respond("Do you sell sunscreen?")
    assert "don't have an answer" in reply


def test_refund_goes_to_a_person():
    assistant = make_assistant()
    reply = assistant.respond("I want a refund")
    assert "store employee" in reply


def test_unknown_request_gets_a_safe_reply():
    assistant = make_assistant()
    reply = assistant.respond("Tell me a joke")
    assert "not sure" in reply


def test_history_grows_by_two_each_turn():
    assistant = make_assistant()
    assistant.respond("hello")
    assistant.respond("What are your hours?")
    assert len(assistant.history) == 4
