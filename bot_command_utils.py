def get_summary_from_message(command, message):
    """Return issue summary string taken from message if there was some command at all"""
    if command in message:
        return message[len(command)+1:] # Get the summary without command itseld and a space(+1)
    else:
        raise TypeError("Somehow there is no bot command in user message")

def get_project_from_message(message, project_command):
    """Return project from message if there was some or returns default one"""
    if project_command in message:
        return message[message.find(project_command)+len(project_command)+1::] # From project command start + space(+1) + project_command
    else:
        return 'FOT' # Default project

def get_assignee_from_message(message, assignee_command):
    """Return assignee from message if there was some or returns default one"""
    if assignee_command in message:
        return message[message.find(assignee_command)+len(assignee_command)+1::] # From assignee command start + space(+1) + assigne command length
    else:
        return 'anatoliy.romsa'
