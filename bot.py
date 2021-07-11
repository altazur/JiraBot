import os
from jira import JIRAError
from JiraAPI import JiraAPI
from slack import WebClient, RTMClient
from bot_command_parser import get_project_from_message, get_summary_from_message, get_assignee_from_message, get_priority_from_message
#Using 'SLACK_BOT_TOKEN' sys env
#Using 'JIRA_LOGIN', 'JIRA_PASSWORD', 'JIRA_URL' sys env

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
JIRA_LOGIN = os.environ['JIRA_LOGIN']
JIRA_PASSWORD = os.environ['JIRA_PASSWORD']
JIRA_URL = os.environ['JIRA_URL']

EXAMPLE_COMMAND = "To create jira issue just type 'create_{issue type} {issue_summary} Project: {Jira project id}(optional) Assignee: {Jira username} (optional)'. For example, 'create_bug This bot stinks'"
CREATE_BUG_COMMAND = "create_bug"
CREATE_TASK_COMMAND = "create_task"
CREATE_STORY_COMMAND = "create_story"
CREATE_IMPROVEMENT_COMMAND = "create_improvement"
ASSIGNEE_COMMAND = "Assignee:"
PROJECT_COMMAND = "Project:"
PRIORITY_COMMAND = "Priority:"
ALL_COMMANDS = [CREATE_BUG_COMMAND, CREATE_TASK_COMMAND, CREATE_STORY_COMMAND, CREATE_IMPROVEMENT_COMMAND, ASSIGNEE_COMMAND, PROJECT_COMMAND] # For get summary method

WELCOME_BLOCK_INTRO = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hi! I'm JiraBot. I'm here to help you create Jira issues right here!"
            }
        }
WELCOME_BLOCK_DIVIDER = {
        "type": "divider"
        }
WELCOME_BLOCK_INSTRUCTIONS = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"To create *bug* write '{CREATE_BUG_COMMAND} [Summary]'\nTo create *task* write '{CREATE_TASK_COMMAND} [Summary]'\nTo create *story* write '{CREATE_STORY_COMMAND} [Summary]\nTo create *improvement* write '{CREATE_IMPROVEMENT_COMMAND} [Summary]\nGood luck! :wink:"
            }
        }

def prepare_issue(issue_type, text):
    """Returns jira issue based on the user message text and type"""
    issue_summary = get_summary_from_message(ALL_COMMANDS, text)
    assignee = get_assignee_from_message(text, ASSIGNEE_COMMAND)
    project = get_project_from_message(text, PROJECT_COMMAND)
    priority = get_priority_from_message(text, PRIORITY_COMMAND)
    new_issue = jira_api.create_task(issue_type, issue_summary, issue_summary, assignee, priority, project)
    return new_issue

def prepeare_bot_response(new_issue):
    return f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the {new_issue.fields.project} backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority. Here's the link: {JIRA_URL}/browse/{new_issue.key}"

@RTMClient.run_on(event="message")
def create_issue(**payload):
    data = payload['data']
    web_client = payload['web_client']
    channel_id = data.get('channel')
    user_id = data.get('user')
    text = data.get('text')

    if text is not None:#This check needed in order to prevent None type startwith checking
        if text.startswith(CREATE_BUG_COMMAND):
            try:
                new_issue = prepare_issue("Bug", text)
                response = prepeare_bot_response(new_issue)
            except JIRAError as e:
                response = e.text 
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_TASK_COMMAND):
            try:
                new_issue = prepare_issue("Task", text)
                response = prepeare_bot_response(new_issue)
            except JIRAError as e:
                response = e.text
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_STORY_COMMAND):
            try:
                new_issue = prepare_issue("Story", text)
                response = prepeare_bot_response(new_issue)
            except JIRAError as e:
                response = e.text
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_IMPROVEMENT_COMMAND):
            try:
                new_issue = prepare_issue("Improvement", text)
                response = prepeare_bot_response(new_issue)
            except JIRAError as e:
                response = e.text
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text and text.lower() == "jirabot_help":
            response = EXAMPLE_COMMAND
            web_client.chat_postMessage(channel=channel_id, blocks=[WELCOME_BLOCK_INTRO, WELCOME_BLOCK_DIVIDER, WELCOME_BLOCK_INSTRUCTIONS])
    else:
        return

@RTMClient.run_on(event="bot_added")
def introduction(**payload):
   data = payload['data']
   channel_id = data.get('channel')
   web_client = payload['web_client']

if __name__=="__main__":
    jira_api = JiraAPI(options={'server':JIRA_URL}, basic_auth=(JIRA_LOGIN,JIRA_PASSWORD))
    print("JiraAPI connected")
    rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
    print("SlackBot connected")
    rtm_client.start()
