from typing import Any, List, Optional

from azure.ai.agents.models import ToolDefinition
from azure.core.exceptions import AzureError

from utils.auth import get_client
from utils.config import get_agent_config


class FoundryAgent:
    def __init__(self, agent_key: str, tool_builders: Optional[List[Any]]):
        """
        agent_key: the key in config.yaml under `agents:`
        tool_builders: list of callables(cfg) -> List[ToolDefinition]
        """
        self.key = agent_key
        self.cfg = get_agent_config(agent_key)
        self.client = get_client()
        self.model = self.cfg["model"]
        self.instructions = self.cfg["instructions"]
        self.test_enabled = self.cfg.get("test", False)
        self.test_query = self.cfg.get("test_query")
        self.tool_builders = tool_builders or []
        self.agent = None

    def _build_tools(self) -> List[ToolDefinition]:
        tools: List[ToolDefinition] = []
        for builder in self.tool_builders:
            tools.extend(builder(self.cfg))
        return tools

    def create(self, name: Optional[str]) -> str:
        """
        Create (or re-create) this agent in Azure Foundry.
        If an agent with `name` already exists:
          - if config.overwrite is true, delete+recreate
          - otherwise, reuse the existing agent
        Returns the agent.id
        """
        name = name or f"{self.key}_agent"
        overwrite = self.cfg.get("overwrite", False)

        existing = [
            a
            for a in self.client.agents.list_agents()  # list all agents in this project
            if a.name == name
        ]

        if existing:
            old = existing[0]
            if overwrite:
                print(f"🔄 Overwrite enabled: deleting existing {self.key} agent ({old.id})")
                self.client.agents.delete_agent(old.id)
            else:
                print(f"♻️ Reusing existing {self.key} agent: {old.id}")
                self.agent = old
                return old.id

        try:
            self.agent = self.client.agents.create_agent(
                model=self.model,
                name=name,
                instructions=self.instructions,
                tools=self._build_tools(),
            )
            assert self.agent is not None
            print(f"✅ {self.key.capitalize()} agent created: {self.agent.id}")
            return self.agent.id

        except AzureError as e:
            raise RuntimeError(f"Failed to create {self.key} agent: {e}")

    def call(self, prompt: str) -> str:
        """
        Send `prompt` to this agent and return the assistant's last message.
        Must call create() first (so self.agent.id exists).
        """
        if not self.agent:
            raise RuntimeError("Agent not created yet. Call `create()` first.")

        thread = self.client.agents.threads.create()

        self.client.agents.messages.create(thread_id=thread.id, role="user", content=prompt)

        run = self.client.agents.runs.create_and_process(
            thread_id=thread.id, agent_id=self.agent.id
        )

        msgs = list(self.client.agents.messages.list(thread_id=thread.id, run_id=run.id))
        return msgs[-1].content

    def test(self):
        """
        If configured, run a sanity check on creation or a test query.
        """
        if not self.test_enabled:
            return
        if self.test_query:
            out = self.call(self.test_query)
            print(f"📝 {self.key.capitalize()} test response:\n{out}")
        else:
            fetched = self.client.agents.get_agent(self.agent.id)
            print(f"🔍 {self.key.capitalize()} fetched OK: {fetched.id}")
