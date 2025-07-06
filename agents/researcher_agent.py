import os

from azure.ai.agents.models import BingGroundingTool

from utils.agent import FoundryAgent


def build_bing_tools(cfg):
    bing_cfg = next((t for t in cfg.get("tools", []) if t["type"] == "bing_grounding"), None)
    if not bing_cfg:
        return []
    conn_id = os.getenv(bing_cfg["connection_env"])
    if not conn_id:
        raise EnvironmentError(f"Set {bing_cfg['connection_env']} in your .env")
    return BingGroundingTool(connection_id=conn_id, count=bing_cfg.get("count", 3)).definitions


class ResearcherAgent(FoundryAgent):
    def __init__(self):
        super().__init__(agent_key="researcher", tool_builders=[build_bing_tools])


if __name__ == "__main__":
    a = ResearcherAgent()
    a.create(name="researcher_agent")
    a.test()
