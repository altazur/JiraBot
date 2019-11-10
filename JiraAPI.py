import os
from jira import JIRA


class JiraAPI(JIRA):
    project = 'FOT'

    def create_task(type='Bug', summary, description, assignee, priority):
        project = self.project(project)
        new_issue_dict = {
                'project': {'id': project.id},
                'summary': summary,
                'description': description,
                'issuetype': {'name': type},
                'priority': priority,
                'assignee': {'displayName', assignee}
                }
        return self.create_issue(fields=new_issue_dict)

