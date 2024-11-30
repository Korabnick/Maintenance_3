import requests
import json

class JiraClient:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as file:
            config = json.load(file)
        self.base_url = config["jira_base_url"]
        self.auth = config.get("auth")
        self.project_key = config["project_key"]

    def get_issues(self, jql, fields=None, expand=None):
        """Получает задачи из JIRA по заданному JQL-запросу."""
        params = {
            "jql": jql,
            "fields": ",".join(fields) if fields else None,
            "expand": ",".join(expand) if expand else None,
            "maxResults": 1000,
        }
        response = requests.get(
            f"{self.base_url}/search",
            params=params,
            auth=self.auth,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching issues: {response.status_code} - {response.text}")

    def get_closed_issues(self, fields=None):
        jql = f"project={self.project_key} AND status=Closed"
        issues = self.get_issues(jql=jql, fields=fields, expand=["changelog"])
        return issues
