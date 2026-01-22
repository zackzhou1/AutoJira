import yaml
from jira import JIRA

def load_config(cfg_file="/home/zzhou/code/config.yaml"):
    with open(cfg_file, "r") as f:
        return yaml.safe_load(f)

def get_jira_client(config=None, cfg_path="/home/zzhou/code/config.yaml"):
    if config is None:
        config = load_config(cfg_path)
    return JIRA(
        server=config["jira_url"],
        basic_auth=(config["email"], config["api_token"])
    )