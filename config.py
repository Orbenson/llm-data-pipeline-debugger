# pipeline_debugger/config.py

import os, yaml
from dotenv import load_dotenv

def load_config(config_path: str) -> dict:
    """Load configuration from a YAML file and overlay environment variables."""
    # Load environment variables from .env file if present
    load_dotenv(os.getenv('ENV_PATH', '.env'))
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    # Overlay any environment-specific overrides if needed (simple case: already handled by dotenv)
    # e.g., if config has placeholders like ${ENV_VAR}, you could resolve them here.
    return config
