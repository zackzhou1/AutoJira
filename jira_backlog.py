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
            "You are a senior development architect. I will provide you a list of backlog tickets as JSON. "
            "Analyze and organize them for sprint and portfolio planning.\n\n"
            "Instructions:\n"
            "1. Remove clearly duplicated or non-actionable tickets.\n"
            "2. List the actionable tickets in a markdown table with these columns and markdown table header:\n"
            "| Key | Summary | Value | Reason | Category |\n"
            "|-----|---------|-------|--------|----------|\n"
            "Each ticket must be one row: Key, a concise summary (8 words max), a value (1-10), a short reason for the value (max 8 words), and one of these categories ONLY (pick the best one):\n"
            "   - Technical Debt\n"
            "   - New Feature\n"
            "   - Bugfix\n"
            "   - Refactor\n"
            "   - Integration\n"
            "   - Customer Request\n"
            "   - Documentation\n"
            "   - Research/Spike\n"
            "   - Other\n"
            "3. Each ticket must only appear once. If tickets are similar or duplicates, only include the main ticket in the table, and mention their keys as duplicates in the summary table for their group.\n"
            "4. After the main ticket markdown table, add a markdown table for each category found with these columns:\n"
            "| Category | Total Value | Ticket IDs | Summary |\n"
            "|----------|------------|------------|---------|\n"
            " - Category: The category name listed above\n"
            " - Total Value: The sum of values for that group\n"
            " - Ticket IDs: All ticket keys in that group, comma-separated\n"
            " - Summary: A 1-3 sentence high-level summary for the group, including a note if any tickets are explicit duplicates (and their keys)\n"
            "5. Do NOT repeat the instructions or input JSON in your answer.\n"
            "6. IMPORTANT: Do not add any conclusions, statements, or additional commentary after the last category table/summary. End the output immediately after the last required markdown table."
            "\n\nHere are the tickets:\n"
            f"{ticket_json}\n"
            "Respond ONLY with the requested markdown tables as described above."
        )
        
        result = generate_text(prompt)
        fname = os.path.join(output_dir, f"batch_{idx:03d}.md")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Wrote summary for batch {idx} to {fname}")

if __name__ == "__main__":
    main()