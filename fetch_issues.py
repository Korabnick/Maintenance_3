import json
from jira_client import JiraClient

if __name__ == "__main__":
    jira = JiraClient()

    fields = ["id", "key", "created", "updated", "status", "assignee", "reporter", "timespent", "priority", "resolutiondate"]
    closed_issues = jira.get_closed_issues(fields=fields)

    # Обогащаем данными из changelog
    closed_issues = jira.get_issues(
        jql="project=HADOOP AND status=Closed",
        fields=fields,
        expand=["changelog"]
    )

    with open("data.json", "w") as file:
        json.dump(closed_issues, file, indent=4)

    print("Закрытые задачи успешно сохранены в data.json.")
