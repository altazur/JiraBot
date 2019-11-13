import os
import time
import re
from JiraAPI import JiraAPI
from slack import WebClient, RTMClient
#Using 'SLACK_BOT_TOKEN' sys env
#Using 'JIRA_LOGIN', 'JIRA_PASSWORD', 'JIRA_URL' sys env

try:
    slack_client = WebClient(os.environ.get('SLACK_BOT_TOKEN'))
    jira_api = JiraAPI(options={'server':str(os.environ.get('JIRA_URL'))}, basic_auth=(str(os.environ.get('JIRA_LOGIN')), str(os.environ.get('JIRA_PASSWORD'))))
except ConnectionError:
    print("Connection error")
jirabot_id = None

RTM_READ_DELAY = 1 #1 seconds to delay between reading
EXAMPLE_COMMAND = "To create jira issue just type 'create_{issue type} {issue_summary}'. For example, 'create_bug This bot stinks'"
#TODO: Change command checks with these constants
CREATE_BUG_COMMAND = "create bug"
CREATE_TASK_COMMAND = "create task"
CREATE_STORY_COMMAND = "create story"
CREATE_IMPROVEMENT_COMMAND = "create improvement"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

@RTMClient.run_on(event="message")
def parse_bot_commands(**payload):
    """Return tuple (message, channel) if there is a bot command"""
    slack_events = payload['data']
    for event in slack_events:
        user_id, message = parse_direct_mention(event["text"])
        if user_id == jirabot_id:
            return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """If there is a mention returns user_id which was mentioned and the text after the mention. Otherwise return (None, None)"""
    matches = re.search(MENTION_REGEX, message_text)
    #The first group contains username, the second - the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def jira_bot_say(message_text, channel):
    """Calling bot response with given text into the given channel"""
    slack_client.api_call("chat.postMessage", channel=channel, text=message_text)

def handle_command(command, channel):
    """Executes command if the command is known"""
    #Default response if the command is wrong"""
    default_response = "*{}*.".format(EXAMPLE_COMMAND)
    response = None

    if command.startswith("create_bug"):
        #Take summary from the command
        issue_summary = command[11:]
        new_issue = jira_api.create_task("Bug", issue_summary, issue_summary, "Anatoliy Romsa", "P3")
        response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority"
    elif command.startwith("create_task"):
        issue_summary = command[12:]
        new_issue = jira_api.create_task("Task", issue_summary, issue_summary, "Anatoliy Romsa", "P3")
        response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority"
    elif command.startwith("create_story"):
        issue_summary = command[13:]
        new_issue = jira_api.create_task("Story", issue_summary, issue_summary, "Anatoliy Romsa", "P3")
        response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority"
    elif command.startwith("create_improvement"):
        issue_summary = command[19:]
        new_issue = jira_api.create_task("Improvement", issue_summary, issue_summary, "Anatoliy Romsa", "P3")
        response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority"
    #Send response to the channel
    slack_client.api_call("chat.postMessage", channel=channel, text=response or default_response)

if __name__ == "__main__":
    """Instantiate bot and 'activatin it' by infinite Loop"""
    if slack_client.rtm_connect(token=os.environ.get('SLACK_BOT_TOKEN')):
        print("JiraBot connected and running")
        jirabot_id = slack_client.api_call("auth.test")["user_id"]
        rtm_client = RTMClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        rtm_client.start()
        while True:
            command, channel = parse_bot_commands()
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection has been lost")
