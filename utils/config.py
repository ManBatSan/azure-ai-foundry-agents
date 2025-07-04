from pathlib import Path

import yaml

_config = None


def load_config():
    global _config
    if _config is None:
        cfg_path = Path(__file__).parent.parent / "agents/config.yaml"
        with open(cfg_path, "r", encoding="utf-8") as f:
            _config = yaml.safe_load(f)
    return _config


def get_agent_config(agent_key: str) -> dict:
    cfg = load_config()
    agents = cfg.get("agents", {})
    if agent_key not in agents:
        raise KeyError(f"Agent '{agent_key}' not found in config.yaml")
    return agents[agent_key]
