from jira_client import load_config, get_jira_client
from jira_actions import get_worked_on_this_week_issues, get_issue_overview_and_comments
from text_gen import generate_text

def main():
    config = load_config()
    jira = get_jira_client(config)
    user_account_id = config["user_account_id"]
    issues = get_worked_on_this_week_issues(jira, user_account_id)

    if not issues:
        print("No tickets worked on this week for this user.")
        return

    print(f"Found {len(issues)} tickets updated this week.")

    overviews = []
    for issue in issues:
        overview = get_issue_overview_and_comments(jira, issue)
        overviews.append(overview)

    # Format context for LLM: Each ticket as a unit, or use a table if you prefer
    ticket_summaries = []
    for o in overviews:
        ticket_summaries.append(
                f"{o['key']} | {o['summary']} | {o['issuetype']} | {o['priority']} | {o['status']} | "
                f"Description: {o['description'] or '[No Description]'} | "
                f"Recent comments: {' | '.join(o['comments'][-3:]) if o['comments'] else '[No Comments]'}"
                )
    tickets_context = "\n".join(ticket_summaries)

    ai_prompt = (
        "Below is a list of Jira tickets worked on this week, including technical context and recent comments.\n"
        "For each ticket, write a very concise, technical one-line summary of recent work or changes, starting with the ticket number. "
        "List all tickets, one line each, no timestamps or author names. "
        "After the summary, create a plan for next week in terms of action items, same format, no bullet points, "
        "no ticket numbers "
        "Avoid boilerplate or repetition — focus on engineering details, implementation, or blockers.\n"
        "Here are the tickets:\n"
        f"{tickets_context}\n"
        "Output:\n"
    )
    try:
        all_summary = generate_text(ai_prompt)
        print("\n=== Weekly Combined Ticket Summaries ===\n")
        print(all_summary)
    except Exception as e:
        print(f"OpenAI failed: {str(e)}. No weekly summary generated.")

if __name__ == "__main__":
    main()