import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)

# TODO: replace with your real details. Kept separate from the RAG knowledge
# base on purpose - these are small, structured lookups (exact links, an
# enumerable project list) that complement free-text RAG search over a
# resume/profile document, rather than duplicating it.
_CONTACT_INFO = {
    "email": "TODO@example.com",
    "linkedin": "https://linkedin.com/in/TODO",
    "github": "https://github.com/TODO",
}

_PROJECTS = [
    {"name": "TODO Project 1", "summary": "TODO one-line description"},
    {"name": "TODO Project 2", "summary": "TODO one-line description"},
]


@tool
def get_contact_info() -> dict:
    """Get contact information: email, LinkedIn, and GitHub links."""
    logger.debug("get_contact_info()")
    return _CONTACT_INFO


@tool
def list_projects() -> list[dict]:
    """List notable projects with a one-line summary of each."""
    logger.debug("list_projects()")
    return _PROJECTS
