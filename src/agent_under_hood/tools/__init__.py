from agent_under_hood.tools.pricing import apply_discount, get_product_price
from agent_under_hood.tools.profile import get_contact_info, list_projects

# ALL_TOOLS: unchanged, used by the CLI's shopping-agent demo.
ALL_TOOLS = [get_product_price, apply_discount]

# PROFILE_TOOLS: for the personal-assistant use case (e.g. the FastAPI
# service backing ask-rakesh-ai) - a different persona, different tools.
PROFILE_TOOLS = [get_contact_info, list_projects]

__all__ = [
    "get_product_price",
    "apply_discount",
    "ALL_TOOLS",
    "get_contact_info",
    "list_projects",
    "PROFILE_TOOLS",
]
