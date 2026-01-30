import json
from jira_actions import get_backlog_issues, get_issue_overview
from text_gen import generate_text
from jira_client import load_config, get_jira_client
import os

def batch_list(items, batch_size):
    """Yield successive batches from a list."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def main():
    config = load_config()
    jira = get_jira_client(config)
    issues = get_backlog_issues(jira, project_key="RDL")
    overviews = [get_issue_overview(issue) for issue in issues]
    print(f"Found {len(overviews)} backlog items.")

    batch_size = 50
    output_dir = "llm_backlog_summaries"
    os.makedirs(output_dir, exist_ok=True)

    for idx, batch in enumerate(batch_list(overviews, batch_size), start=1):
        ticket_json = json.dumps(batch, indent=2)
        prompt = (
            "You are a senior development architect. I will provide a list of backlog tickets as JSON. "
            "Analyze and organize them for sprint and portfolio planning.\n\n"
            "Instructions:\n"
            "1. Remove clearly duplicated or non-actionable tickets.\n"
            "2. List the actionable tickets in a markdown table with these columns and header:\n"
            "| Key | Summary | Value | Reason | Category |\n"
            "|-----|---------|-------|--------|----------|\n"
            "For each ticket:\n"
            " - Key: The ticket key/ID.\n"
            " - Summary: Up to 12 words. If client or operational impact, briefly state the affected area or effect. For tech debt/refactor, specify the subsystem or area.\n"
            " - Value: 1–10, according to this rubric:\n"
            "     • 8–10: Direct client impact or affects client-facing operations or urgent for business continuity.\n"
            "     • 5–7: Critical operational value, major internal process.\n"
            "     • 2–4: Enhancements, minor improvements, or internal efficiency.\n"
            "     • 1: Technical debt, refactoring, or routine maintenance (unless it unblocks higher-value work).\n"
            " - Reason: Evaluate using both the value according to the rubric as well as the priority and story points. Be concise but descriptive\n"
            " - Category: Choose only from:\n"
            "   - Technical Debt\n"
            "   - New Feature\n"
            "   - Bugfix\n"
            "   - Refactor\n"
            "   - Integration\n"
            "   - Customer Request\n"
            "   - Documentation\n"
            "   - Research/Spike\n"
            "   - Other\n"
            "3. Each ticket must appear only once. If similar/duplicate, show only main ticket and note duplicates in the summary table for the group.\n"
            "4. After the main table, add a markdown table for each found category with these columns:\n"
            "| Category | Total Value | Ticket IDs | Summary |\n"
            "|----------|------------|------------|---------|\n"
            "5. Do NOT repeat the instructions or input JSON in your answer.\n"
            "6. IMPORTANT: Do not add any conclusions, statements, or commentary after the last table. End immediately after the last summary.\n"
            "\nHere are the tickets:\n"
            f"{ticket_json}\n"
            "Respond ONLY with the requested markdown tables as described above."
        )
        
        result = generate_text(prompt)
        fname = os.path.join(output_dir, f"batch_{idx:03d}.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Wrote summary for batch {idx} to {fname}")
        exit(0)  # For testing, process only one batch

if __name__ == "__main__":
    main()