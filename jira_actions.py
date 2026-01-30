import json
def get_in_progress_issues(jira, user_account_id):
    jql = f'assignee = "{user_account_id}" AND status = "In Progress"'
    print(jql)
    return jira.enhanced_search_issues(jql)

def add_comment_to_issue(jira, issue_key, comment):
    jira.add_comment(issue_key, comment)

def get_issue_description(jira, issue_key):
    issue = jira.issue(issue_key)
    return issue.fields.summary, issue.fields.description

def test_jira_connection(jira):
    try:
        myself = jira.myself()
        print(f"Successfully connected as: {myself['displayName']} ({myself['emailAddress']})")
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    
def get_issue_comments(jira, issue):
    """Return a list of comment objects for a given issue"""
    return jira.comments(issue)

def extract_comment_body(comment):
    """Extract plain text from a Jira comment, regardless of format."""
    body = comment.body
    if isinstance(body, str):
        return body.strip()
    # If it's Atlassian Document Format, merge all text content
    if isinstance(body, dict) and 'content' in body:
        def parse_adf(adf_nodes):
            text_parts = []
            for node in adf_nodes:
                # Recursively extract text
                if node.get('type') == 'text' and 'text' in node:
                    text_parts.append(node['text'])
                elif 'content' in node:
                    text_parts.extend(parse_adf(node['content']))
            return text_parts
        if 'content' in body:
            return ' '.join(parse_adf(body['content'])).strip()
    # fallback
    return str(body).strip()

def get_last_n_comment_bodies(jira, issue, n=3):
    """Return the text of the last n comments for an issue as a single formatted string."""
    comments = jira.comments(issue)
    if not comments:
        return "No previous comments."
    selected = comments[-n:]  # Last n comments
    bodies = [extract_comment_body(comment) for comment in selected]
    return "\n".join(bodies)

def get_backlog_issues(jira, project_key="RDL", status_names=("To Do", "Open")):
    status_str = ", ".join([f'"{status}"' for status in status_names])
    jql = f'project = {project_key} AND status in ({status_str}) AND created >= -104w ORDER BY created DESC'

    print("Fetching backlog issues with JQL:", jql)
    all_issues = []
    next_page_token = None

    while True:
        if next_page_token:
            page = jira.enhanced_search_issues(jql, nextPageToken=next_page_token)
        else:
            page = jira.enhanced_search_issues(jql)
        
        # page is a list of issues (not a dict)
        all_issues.extend(page)

        # The nextPageToken is an attribute on the result list (not a dict key on resp)
        # This is a trick with recent versions of jira-python: check for _nextPageToken
        next_page_token = getattr(page, "nextPageToken", None)
        if not next_page_token:
            break

    return all_issues

def get_issue_overview(issue):
    fields = issue.fields
    result = {
        "priority": getattr(fields.priority, "name", "") if hasattr(fields, "priority") else "",
        "story_points": getattr(fields, "customfield_10004", None),  # use None, 0, or '' as default
        "key": issue.key,
        "summary": getattr(fields, "summary", ""),
        "created": getattr(fields, "created", ""),
        "issuetype": getattr(fields.issuetype, "name", ""),
        "description": getattr(fields, "description", ""),
        "status": getattr(fields.status, "name", ""),
        "reporter": getattr(fields.reporter, "displayName", "") if hasattr(fields, "reporter") else "",
        "assignee": getattr(fields.assignee, "displayName", "") if hasattr(fields, "assignee") else "",
    }
    print(json.dumps(result, indent=2))  # Pretty-print as JSON
    return result

def get_worked_on_this_week_issues(jira, user_account_id):
    jql = (
        f'assignee = "{user_account_id}" '
        f'AND updated >= startOfWeek() '
        f'ORDER BY updated DESC'
    )
    print(f"JQL: {jql}")
    return list(jira.enhanced_search_issues(jql))

def get_issue_overview_and_comments(jira, issue):
    fields = issue.fields
    # Get all comment bodies
    comments = jira.comments(issue)
    comments_bodies = [comment.body.strip() if hasattr(comment, 'body') else str(comment) for comment in comments]
    result = {
        "priority": getattr(fields.priority, "name", "") if hasattr(fields, "priority") else "",
        "story_points": getattr(fields, "customfield_10004", None),
        "key": issue.key,
        "summary": getattr(fields, "summary", ""),
        "created": getattr(fields, "created", ""),
        "updated": getattr(fields, "updated", ""),
        "issuetype": getattr(fields.issuetype, "name", ""),
        "description": getattr(fields, "description", ""),
        "status": getattr(fields.status, "name", ""),
        "reporter": getattr(fields.reporter, "displayName", "") if hasattr(fields, "reporter") else "",
        "assignee": getattr(fields.assignee, "displayName", "") if hasattr(fields, "assignee") else "",
        "comments": comments_bodies,
        }
    return result

