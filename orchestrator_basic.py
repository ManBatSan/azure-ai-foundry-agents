# agents/orchestrator.py

import os

from azure.ai.agents.models import ConnectedAgentDetails, ConnectedAgentToolDefinition
from azure.core.exceptions import AzureError

from utils.auth import get_client


def main():
    client = get_client()

    # IDs of your pre-created agents
    researcher_id = os.getenv("RESEARCHER_AGENT_ID")
    writer_id = os.getenv("WRITER_AGENT_ID")

    # Define connected agent tools
    research_tool = ConnectedAgentToolDefinition(
        connected_agent=ConnectedAgentDetails(
            id=researcher_id,
            name="researcher_agent",
            description=(
                "Use this tool to fetch and summarize facts from Bing Search "
                "when you need more background information."
            ),
        )
    )

    write_tool = ConnectedAgentToolDefinition(
        connected_agent=ConnectedAgentDetails(
            id=writer_id,
            name="writer_agent",
            description=("Use this tool to draft a coherent article from provided facts."),
        )
    )

    # Create the orchestrator agent
    try:
        orchestrator = client.agents.create_agent(
            model="gpt-4o-mini",
            name="qa_orchestrator",  # also use underscores if you want consistency
            instructions=(
                "You are an orchestrator. First use the research tool to get facts, "
                "then use the write tool to draft the article. "
                "If you need more context, call the research tool again."
            ),
            tools=[research_tool, write_tool],
        )
        print(f"✅ Orchestrator agent created: {orchestrator.id}")
    except AzureError as e:
        print(f"❌ Failed to create orchestrator: {e}")
        return

    # Test it
    try:
        thread = client.agents.threads.create()
        client.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content="What drives the recent surge in electric vehicle adoption?",
        )
        run = client.agents.runs.create_and_process(thread_id=thread.id, agent_id=orchestrator.id)
        msgs = list(client.agents.messages.list(thread_id=thread.id, run_id=run.id))
        print("📰 Orchestrator final reply:")
        print(msgs[-1].content)
    except AzureError as e:
        print(f"❌ Orchestrator test failed: {e}")


if __name__ == "__main__":
    main()
