from jira_client import JiraClient

jira = JiraClient()
issues = jira.get_issues(jql="project=HADOOP AND status=Closed", fields=["id", "key", "created", "updated"])
for issue in issues["issues"]:
    print(issue["key"], issue["fields"]["created"], issue["fields"]["updated"])
