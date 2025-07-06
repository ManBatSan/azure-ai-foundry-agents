from utils.agent import FoundryAgent


class WriterAgent(FoundryAgent):
    def __init__(self):
        super().__init__(agent_key="writer")


if __name__ == "__main__":
    a = WriterAgent()
    a.create(name="writer_agent")
    a.test()
