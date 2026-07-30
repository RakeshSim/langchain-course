import logging

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langsmith import traceable

from agent_under_hood.config import settings
from agent_under_hood.tools import ALL_TOOLS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a helpful shopping assistant. "
    "You have access to a product catalog tool "
    "and a discount tool.\n\n"
    "STRICT RULES — you must follow these exactly:\n"
    "1. NEVER guess or assume any product price. "
    "You MUST call get_product_price first to get the real price.\n"
    "2. Only call apply_discount AFTER you have received "
    "a price from get_product_price. Pass the exact price "
    "returned by get_product_price — do NOT pass a made-up number.\n"
    "3. NEVER calculate discounts yourself using math. "
    "Always use the apply_discount tool.\n"
    "4. If the user does not specify a discount tier, "
    "ask them which tier to use — do NOT assume one."
)


class AgentError(Exception):
    """Raised when the agent loop cannot produce an answer."""


@traceable(name="LangChain Agent Loop")
def run_agent(
    question: str,
    history: list[BaseMessage] | None = None,
    system_prompt: str = SYSTEM_PROMPT,
    tools: list | None = None,
) -> str:
    """Run the tool-calling agent loop.

    `history` and `system_prompt`/`tools` are optional so existing callers
    (the CLI, the tests) get the exact original single-shot shopping-agent
    behavior unchanged. A caller with a different persona (e.g. a RAG-backed
    personal-assistant service) passes its own system_prompt/tools and prior
    conversation turns via `history`.
    """
    tool_list = tools if tools is not None else ALL_TOOLS
    tools_dict = {t.name: t for t in tool_list}

    llm = init_chat_model(settings.agent_model, temperature=0)
    llm_with_tools = llm.bind_tools(tool_list)

    logger.info("question: %s", question)

    messages: list[BaseMessage] = [SystemMessage(content=system_prompt)]
    if history:
        messages.extend(history)
    messages.append(HumanMessage(content=question))

    for iteration in range(1, settings.max_iterations + 1):
        logger.info("iteration %d", iteration)

        ai_message = llm_with_tools.invoke(messages)
        tool_calls = ai_message.tool_calls

        if not tool_calls:
            logger.info("final answer produced")
            return ai_message.content

        tool_call = tool_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_call_id = tool_call.get("id")

        logger.info("tool selected: %s(%s)", tool_name, tool_args)

        tool_to_use = tools_dict.get(tool_name)
        messages.append(ai_message)

        if tool_to_use is None:
            logger.warning("unknown tool requested: %s", tool_name)
            messages.append(
                ToolMessage(
                    content=f"Error: tool '{tool_name}' does not exist.",
                    tool_call_id=tool_call_id,
                )
            )
            continue

        try:
            observation = tool_to_use.invoke(tool_args)
            logger.info("tool result: %s", observation)
            messages.append(
                ToolMessage(content=str(observation), tool_call_id=tool_call_id)
            )
        except Exception as exc:
            # Fed back to the LLM as the tool result, not raised — lets the
            # model see what went wrong and recover (e.g. retry with a
            # valid argument) instead of crashing the whole run.
            logger.warning("tool '%s' failed: %s", tool_name, exc)
            messages.append(
                ToolMessage(content=f"Error: {exc}", tool_call_id=tool_call_id)
            )

    raise AgentError(f"No final answer after {settings.max_iterations} iterations")
