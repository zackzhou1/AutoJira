from jira_client import load_config, get_jira_client
from jira_actions import test_jira_connection

def test_connection():
    config = load_config()
    jira = get_jira_client(config)
    assert test_jira_connection(jira), "Connection to Jira failed!"

if __name__ == "__main__":
    test_connection()