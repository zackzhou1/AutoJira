import json
from jira_client import load_config, get_jira_client
from jira_actions import get_in_progress_issues

def recursive_serialize(obj, max_depth=4, depth=0, seen=None):
    if seen is None:
        seen = set()
    if depth > max_depth:
        return f"[Max depth {max_depth} reached]"
    if id(obj) in seen:
        return "[Circular Reference]"
    seen.add(id(obj))
    if hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            # convert all keys to string
            result[str(key)] = recursive_serialize(value, max_depth, depth + 1, seen)
        return result
    elif isinstance(obj, dict):
        return {str(k): recursive_serialize(v, max_depth, depth + 1, seen) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_serialize(i, max_depth, depth + 1, seen) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(recursive_serialize(i, max_depth, depth + 1, seen) for i in obj)
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # For anything else, just coerce to string
        return str(obj)

def print_issue_fields(issue):
    """Print the full Jira fields structure for an issue."""
    try:
        fields_dict = vars(issue.fields)
    except Exception:
        fields_dict = issue.fields
    structure = recursive_serialize(fields_dict)
    print(json.dumps(structure, indent=2, default=str))

def main():
    config = load_config()
    jira = get_jira_client(config)
    user = config["user_account_id"] if "user_account_id" in config else None

    issues = get_in_progress_issues(jira, user)
    if not issues:
        print("No 'In Progress' tickets found for this user.")
        return

    for issue in issues:
        print(f"\n--- Ticket: {issue.key} ---")
        print_issue_fields(issue)
        print("\n")  # Visual separation

if __name__ == "__main__":
    main()