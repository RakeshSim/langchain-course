import logging

import click
from dotenv import load_dotenv

from agent_under_hood.agent import AgentError, run_agent
from agent_under_hood.logging_config import configure_logging

logger = logging.getLogger(__name__)


@click.command()
@click.argument("question")
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging.")
def main(question: str, verbose: bool) -> None:
    """Ask the shopping assistant agent a QUESTION."""
    load_dotenv()
    configure_logging(level=logging.DEBUG if verbose else logging.INFO)

    try:
        answer = run_agent(question)
    except AgentError as exc:
        logger.error("agent failed: %s", exc)
        raise SystemExit(1) from exc

    click.echo(f"\n{answer}")


if __name__ == "__main__":
    main()
