import os

from azure.ai.agents.models import BingGroundingTool
from azure.core.exceptions import AzureError

from utils.auth import get_client
from utils.config import get_agent_config


def main():
    # 1. Load config
    cfg = get_agent_config("researcher")
    model = cfg["model"]
    instr = cfg["instructions"]
    tools_cfg = cfg.get("tools", [])
    test_enabled = cfg.get("test", False)
    test_query = cfg.get("test_query")

    # 2. Authenticate
    client = get_client()

    # 3. Build tools list
    tool_defs = []
    for t in tools_cfg:
        if t["type"] == "bing_grounding":
            conn_id = os.getenv(t["connection_env"])
            if not conn_id:
                raise EnvironmentError(f"Set {t['connection_env']} in .env")
            tool_defs.extend(
                BingGroundingTool(connection_id=conn_id, count=t.get("count", 3)).definitions
            )

    # 4. Create the agent
    try:
        print(tool_defs)
        agent = client.agents.create_agent(
            model=model, name="researcher-agent", instructions=instr, tools=tool_defs
        )
        print(f"✅ Researcher agent created: {agent.id}")
    except AzureError as e:
        print(f"❌ Failed to create researcher agent: {e}")
        return

    # 5. Optional test run
    if test_enabled and test_query:
        try:
            thread = client.agents.threads.create()
            client.agents.messages.create(thread_id=thread.id, role="user", content=test_query)
            run = client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            msgs = client.agents.messages.list(thread_id=thread.id, run_id=run.id)
            last = list(msgs)[-1]
            print("📝 Researcher response:")
            print(last.content)
        except AzureError as e:
            print(f"❌ Researcher test failed: {e}")


if __name__ == "__main__":
    main()
