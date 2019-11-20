import os
from JiraAPI import JiraAPI
from slack import WebClient, RTMClient
#Using 'SLACK_BOT_TOKEN' sys env
#Using 'JIRA_LOGIN', 'JIRA_PASSWORD', 'JIRA_URL' sys env

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
JIRA_LOGIN = os.environ['JIRA_LOGIN']
JIRA_PASSWORD = os.environ['JIRA_PASSWORD']
JIRA_URL = os.environ['JIRA_URL']

EXAMPLE_COMMAND = "To create jira issue just type 'create_{issue type} {issue_summary}'. For example, 'create_bug This bot stinks'"
CREATE_BUG_COMMAND = "create_bug"
CREATE_TASK_COMMAND = "create_task"
CREATE_STORY_COMMAND = "create_story"
CREATE_IMPROVEMENT_COMMAND = "create_improvement"

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

@RTMClient.run_on(event="message")
def create_issue(**payload):
    data = payload['data']
    web_client = payload['web_client']
    channel_id = data.get('channel')
    user_id = data.get('user')
    text = data.get('text')

    if text is not None:#This check needed in order to prevent None type startwith checking

        if text.startswith(CREATE_BUG_COMMAND):
            issue_summary = text[11:]
            new_issue = jira_api.create_task("Bug", issue_summary, issue_summary, "Anatoliy.Romsa", "P3")
            response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority. Here's the link: {JIRA_URL}/browse/{new_issue.key}"
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_TASK_COMMAND):
            issue_summary = text[12:]
            new_issue = jira_api.create_task("Task", issue_summary, issue_summary, "Anatoliy.Romsa", "P3")
            response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority. Here's the link: {JIRA_URL}/browse/{new_issue.key}"
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_STORY_COMMAND):
            issue_summary = text[13:]
            new_issue = jira_api.create_task("Story", issue_summary, issue_summary, "Anatoliy.Romsa", "P3")
            response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority. Here's the link: {JIRA_URL}/browse/{new_issue.key}"
            web_client.chat_postMessage(channel=channel_id, text=response)
        elif text.startswith(CREATE_IMPROVEMENT_COMMAND):
            issue_summary = text[19:]
            new_issue = jira_api.create_task("Improvement", issue_summary, issue_summary, "Anatoliy.Romsa", "P3")
            response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority. Here's the link: {JIRA_URL}/browse/{new_issue.key}"
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
    #TODO:Infinite loop due to the "message" event is the any message in the channel. Even the bot response. So he is starting talk to himself :)
