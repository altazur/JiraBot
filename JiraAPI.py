import os
from jira import JIRA


class JiraAPI(JIRA):

    def create_task(self, issue_type, summary, description, assignee, priority, project_name='FOT'):
        project = self.project(project_name)#Calling parent JIRA.project func and passing the our project name into it
        new_issue_dict = {
                'project': {'id': project.id},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
                'priority': {'name':priority},
                'assignee': {'name': assignee}
                }
        return self.create_issue(fields=new_issue_dict)

