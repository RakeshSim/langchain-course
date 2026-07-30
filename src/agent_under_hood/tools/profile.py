import logging

from langchain.tools import tool

logger = logging.getLogger(__name__)

# Kept separate from the RAG knowledge base on purpose - these are small,
# structured lookups (exact links, an enumerable project list) that
# complement free-text RAG search over the resume/profile document, rather
# than duplicating it. Deliberately no phone number here - contact info
# returned by this tool can get echoed straight back to anyone chatting
# with the bot, and a phone number is more sensitive than email/LinkedIn
# for that kind of unrestricted exposure.
_CONTACT_INFO = {
    "email": "rakesh.qwert@gmail.com",
    "linkedin": "https://linkedin.com/in/rakesh-yadav-qwert",
    "github": "https://github.com/RakeshSim",
}

_PROJECTS = [
    {
        "name": "Delta Raider & Dymond GUI Revenue Management Platform",
        "summary": "Led the AWS lift-and-shift migration of Delta's revenue management platform from IBM App Server/DB2, with zero-downtime cutover.",
    },
    {
        "name": "FDA Drug Review System (Integrity and Search 360)",
        "summary": "Architected a microservices-based regulatory review system using the Saga pattern across 4 services with full audit traceability via Jaeger.",
    },
    {
        "name": "FedEx Route Optimization Engine (DWS & GDP)",
        "summary": "Designed a route optimization engine using Vehicle Routing Problem (VRP) algorithms to reduce transportation costs.",
    },
    {
        "name": "AI Personal Assistant Agent",
        "summary": "Multi-tool AI agent (LangChain + MCP) integrating 11+ real-world APIs (GitHub, Gmail, Calendar, Slack, Maps) with persistent memory.",
    },
    {
        "name": "Documentation-Based RAG Chatbot",
        "summary": "RAG chatbot enabling analysts to ask natural-language questions and retrieve answers directly from official documentation.",
    },
    {
        "name": "Competitor Analysis Multi-Agent RAG System",
        "summary": "Sequential-workflow multi-agent RAG system benchmarking a company against industry rivals using live web data.",
    },
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
