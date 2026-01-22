import argparse
from jira_client import load_config, get_jira_client
from jira_actions import (
    get_in_progress_issues,
    add_comment_to_issue,
    get_issue_description,
    test_jira_connection,
)

def main():
    parser = argparse.ArgumentParser(description="Jira CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # List 'In Progress'
    subparsers.add_parser("list-inprogress", help="List all 'In Progress' tickets assigned to the user")

    # Add comment
    c_parser = subparsers.add_parser("add-comment", help="Add a comment to a Jira issue")
    c_parser.add_argument("issue_key", help="Jira issue key (e.g., PROJ-123)")
    c_parser.add_argument("comment", help="Comment to add")

    # Get description
    d_parser = subparsers.add_parser("get-description", help="Retrieve summary & description of an issue")
    d_parser.add_argument("issue_key", help="Jira issue key (e.g., PROJ-123)")

    # Test connection
    subparsers.add_parser("test", help="Test connection to JIRA.")

    args = parser.parse_args()
    config = load_config()
    jira = get_jira_client(config=config)

    if args.command == "list-inprogress":
        issues = get_in_progress_issues(jira, config["user_account_id"])
        if issues:
            print("Issues in progress:")
            for issue in issues:
                print(f"{issue.key}: {issue.fields.summary}")
        else:
            print("No 'In Progress' tickets found for this user.")

    elif args.command == "add-comment":
        try:
            add_comment_to_issue(jira, args.issue_key, args.comment)
            print(f"Comment added to {args.issue_key}.")
        except Exception as e:
            print(f"Failed to add comment: {e}")

    elif args.command == "get-description":
        try:
            summary, desc = get_issue_description(jira, args.issue_key)
            print(f"Summary: {summary}\nDescription:\n{desc}")
        except Exception as e:
            print(f"Could not retrieve issue: {e}")

    elif args.command == "test":
        test_jira_connection(jira)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()