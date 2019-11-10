import os
import time
import re
from slackclient import SlackClient
import JiraAPI
#Using 'SLACK_BOT_TOKEN' sys env
#Using 'JIRA_LOGIN', 'JIRA_PASSWORD', 'JIRA_URL' sys env

slack_client = SlackClient(os.environ('SLACK_BOT_TOKEN'))
jira_api = JiraAPI(options={'server':str(os.environ('JIRA_URL'))}, basic_auth=(str(os.environ('JIRA_LOGIN')), str(os.environ('JIRA_PASSWORD'))))
jirabot_id = None

RTM_READ_DELAY = 1 #1 seconds to delay between reading
EXAMPLE_COMMAND = "create bug Summary Description 6.5"
CREATE_BUG_COMMAND = "create bug"
CREATE_TASK_COMMAND = "create task"
CREATE_STORY_COMMAND = "create story"
CREATE_IMPROVEMENT_COMMAND = "create improvement"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

if __name__ == "__main__":
    """Instantiate bot and 'activatin it' by infinite Loop"""
    if slack_client.rtm_connect(with_team_state=False):
        print("JiraBot connected and running")
        jirabot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection has been lost")

def parse_bot_commands(slack_events):
    """Return tuple (message, channel) if there is a bot command"""
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == jirabot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """If there is a mention returns user_id which was mentioned and the text after the mention. Otherwise return (None, None)"""
    matches = re.search(MENTION_REGEX, message_text)
    #The first group contains username, the second - the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """Executes command if the command is known"""
    #Default response if the command is wrong"""
    default_response = "I'm sorry, but the command isn't right. Try *{}*.".format(EXAMPLE_COMMAND)
    response = None

    #Issue fields taken from command
    issue_type = None
    issue_summary = None
    issue_description = None
    issue_assigne = None
    issue_priority = None

    if command.startswith("create"):
        #TODO:Split command into issue fields according to sense (not just whitespaces or smth)Maybe only two parameters can be obtained through commands
        #Like "create_bug {Summary}.Should've done that way for now
        new_issue = jira_api.create_task(type="Bug", "Sample bug created by bot", "Description of the sample bug created by bot", "Anatoliy Romsa", "P3")
        response = f"The {new_issue.fields.issuetype} {new_issue.key} has been added to the backlog with {new_issue.fields.assignee} assignment and {new_issue.fields.priority} priority"
    #Send response to the channel
    slack_client.api_call("chat.postMessage", channel=channel, text=response or default_response)
