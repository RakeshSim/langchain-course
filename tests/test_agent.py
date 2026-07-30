from unittest.mock import patch

import pytest
from langchain_core.messages import AIMessage, ToolMessage

from agent_under_hood.agent import AgentError, run_agent


class _FakeLLMWithTools:
    """Stands in for llm.bind_tools(...) - returns canned AIMessages in
    order, but first enforces the same rule the real OpenAI API enforces:
    every tool_call_id from a prior AIMessage must have a matching
    ToolMessage before the next call, or this raises - otherwise a bug
    like "only tool_calls[0] ever gets answered" would pass silently
    against a fake that doesn't check, while failing for real in
    production against the actual API.
    """

    def __init__(self, responses):
        self._responses = iter(responses)

    def invoke(self, messages):
        for i, msg in enumerate(messages):
            if isinstance(msg, AIMessage) and msg.tool_calls:
                answered_ids = {
                    m.tool_call_id
                    for m in messages[i + 1 :]
                    if isinstance(m, ToolMessage)
                }
                expected_ids = {tc["id"] for tc in msg.tool_calls}
                missing = expected_ids - answered_ids
                assert not missing, (
                    f"tool_call_id(s) {missing} were never answered with a "
                    "ToolMessage before the next call"
                )
        return next(self._responses)


class _FakeLLM:
    def __init__(self, responses):
        self._responses = responses

    def bind_tools(self, tools):
        return _FakeLLMWithTools(self._responses)


def _patched_init_chat_model(responses):
    return patch(
        "agent_under_hood.agent.init_chat_model", return_value=_FakeLLM(responses)
    )


def test_run_agent_happy_path_calls_tools_in_order_and_returns_final_answer():
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_product_price",
                    "args": {"product": "laptop"},
                    "id": "call_1",
                }
            ],
        ),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "apply_discount",
                    "args": {"price": 1299.99, "discount_tier": "gold"},
                    "id": "call_2",
                }
            ],
        ),
        AIMessage(content="The final price is $1000.99.", tool_calls=[]),
    ]

    with _patched_init_chat_model(responses):
        answer = run_agent("What is the price of a laptop after a gold discount?")

    assert answer == "The final price is $1000.99."


def test_run_agent_recovers_from_a_failing_tool_call():
    # First call uses a bad product name (tool raises ValueError), second
    # call retries with a valid one - the loop should survive the error
    # and still reach a final answer instead of crashing.
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_product_price",
                    "args": {"product": "smartphone"},
                    "id": "call_1",
                }
            ],
        ),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_product_price",
                    "args": {"product": "laptop"},
                    "id": "call_2",
                }
            ],
        ),
        AIMessage(content="The laptop costs $1299.99.", tool_calls=[]),
    ]

    with _patched_init_chat_model(responses):
        answer = run_agent("How much is a laptop?")

    assert answer == "The laptop costs $1299.99."


def test_run_agent_handles_multiple_tool_calls_in_a_single_turn():
    # A model can request several independent tools in one turn (e.g. two
    # unrelated lookups for a single question). Every tool_call_id must get
    # a response before the next request, or the real OpenAI API rejects
    # the following request with a 400 - reproduces a bug found via manual
    # testing where only tool_calls[0] ever got answered.
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_product_price",
                    "args": {"product": "laptop"},
                    "id": "call_1",
                },
                {
                    "name": "get_product_price",
                    "args": {"product": "keyboard"},
                    "id": "call_2",
                },
            ],
        ),
        AIMessage(
            content="A laptop is $1299.99 and a keyboard is $89.50.",
            tool_calls=[],
        ),
    ]

    with _patched_init_chat_model(responses):
        answer = run_agent("What do a laptop and a keyboard cost?")

    assert answer == "A laptop is $1299.99 and a keyboard is $89.50."


def test_run_agent_raises_agent_error_when_max_iterations_exceeded():
    # Every response asks for another tool call, never gives a final
    # answer - the loop should stop and raise rather than looping forever.
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_product_price",
                    "args": {"product": "laptop"},
                    "id": f"call_{i}",
                }
            ],
        )
        for i in range(20)
    ]

    with _patched_init_chat_model(responses), pytest.raises(AgentError):
        run_agent("loop forever")
