import os

from semantic_kernel.functions import kernel_function

from agents.researcher_agent import ResearcherAgent
from agents.writer_agent import WriterAgent


class FoundryAgentsPlugin:
    def __init__(self):
        self.researcher_id = os.getenv("RESEARCHER_AGENT_ID")
        self.writer_id = os.getenv("WRITER_AGENT_ID")

    @kernel_function(description="Use Bing to fetch and summarize relevant information.")
    def ResearcherSkill(self, query: str) -> str:
        agent = ResearcherAgent()
        agent.agent = agent.client.agents.get_agent(self.researcher_id)
        return agent.call(query)

    @kernel_function(description="Draft a coherent article from provided research summaries.")
    def WriterSkill(self, summary: str) -> str:
        agent = WriterAgent()
        agent.agent = agent.client.agents.get_agent(self.writer_id)
        return agent.call(summary)
