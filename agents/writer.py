from azure.core.exceptions import AzureError

from utils.auth import get_client
from utils.config import get_agent_config


def main():
    # 1. Load config
    cfg = get_agent_config("writer")
    model = cfg["model"]
    instr = cfg["instructions"]
    test_enabled = cfg.get("test", False)

    # 2. Authenticate
    client = get_client()

    # 3. Create the writer agent
    try:
        agent = client.agents.create_agent(
            model=model,
            name="writer-agent",
            instructions=instr,
        )
        print(f"✅ Writer agent created: {agent.id}")
    except AzureError as e:
        print(f"❌ Failed to create writer agent: {e}")
        return

    # 4. Optional sanity check
    if test_enabled:
        try:
            # Simple “sanity”: list this agent by ID to confirm it exists
            fetched = client.agents.get_agent(agent.id)
            print("🔍 Writer agent fetched successfully:", fetched.id)
        except AzureError as e:
            print(f"❌ Writer test failed: {e}")


if __name__ == "__main__":
    main()
