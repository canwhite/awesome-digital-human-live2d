import os
from pathlib import Path

def replace_openai_key(api_key: str):
    """Replace ${OPENAI_API_KEY} in config files with actual API key"""
    
    # Paths to config files
    api_yaml = Path("configs/engines/llm/openaiAPI.yaml")
    agent_yaml = Path("configs/agents/openaiAgent.yaml")
    
    # Read and replace in openaiAPI.yaml
    if api_yaml.exists():
        with open(api_yaml, "r") as f:
            content = f.read()
        content = content.replace("--", api_key)
        with open(api_yaml, "w") as f:
            f.write(content)
    
    # Read and replace in openaiAgent.yaml
    if agent_yaml.exists():
        with open(agent_yaml, "r") as f:
            content = f.read()
        content = content.replace("--", api_key)
        with open(agent_yaml, "w") as f:
            f.write(content)

def load_and_replace():
    """Load API key from .env and replace in config files"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    api_key = line.strip().split("=")[1]
                    replace_openai_key(api_key)
                    break
