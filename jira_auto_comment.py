from jira_client import load_config, get_jira_client
from jira_actions import get_in_progress_issues, get_issue_description, add_comment_to_issue,get_issue_comments, get_last_n_comment_bodies
from text_gen import generate_text
import random

# Place this near your imports
BACKUP_COMMENTS = [
    "Progress made on this ticket.",
    "Work ongoing, no major blockers.",
    "Some integration issues, still making progress.",
    "Investigating a few internal blockers.",
    "Task is moving forward as planned.",
    "Awaiting on input from other teams.",
    "Some challenges faced, continuing work.",
    "Advancing steadily with minor interruptions."
]

def main():
    config = load_config()
    jira = get_jira_client(config)

    # Step 1: Get all in-progress assigned tickets
    issues = get_in_progress_issues(jira, config["user_account_id"])
    if not issues:
        print("No 'In Progress' tickets found for this user.")
        return

    print(f"Found {len(issues)} in-progress ticket(s).")
    
    for issue in issues:
        key = issue.key
        summary, description = get_issue_description(jira, key)
        print(f"\n--- Ticket: {key} ---")
        print(f"Summary: {summary}")
        print(f"Description: {description}")
        
        comment_history = get_last_n_comment_bodies(jira, issue, n=3)  # Get last 3 (adjust n as needed)
        print(f"Recent Comments:\n{comment_history}\n")
        # Step 2: Use description to get OpenAI-generated comment
        ai_prompt = (
            f"Please write a very brief update that relates to some function of this ticket, context below \n"
            f"it needs to be vague. It needs to be short. No timestamps, no authors. It needs to be human readable. \n"
            f"The goal is that every comment should fit after every other comment \n"
            f"generally comment should be successful, with occasional mentions of integration issues or internal blockers.  \n"
            f"Ticket summary: {summary}\n"
            f"Ticket description: {description if description else '[No Description Provided]'}"
            f"Recent comments on this ticket:\n{comment_history}\n"
        )
        try:
            comment = generate_text(ai_prompt)
        except Exception as e:
            print(f"OpenAI failed ({str(e)}). Using backup comment.")
            comment = random.choice(BACKUP_COMMENTS)
        
        print(f"Generated comment:\n{comment}\n")

        # Step 3: Add the comment
        add_comment_to_issue(jira, key, comment)
        print(f"Comment added to {key}.")

if __name__ == "__main__":
    main()
    

