def get_summary_from_message(commands: list, message):
    """Return issue summary string taken from message if there was some command at all. List of all avaluable commands are necessarry due to the 
    function return everything but the commands and their value"""
    if commands is not None:
        message_words = message.split(" ")
        for index, word in enumerate(message_words):
            if word in commands:
                if "_" in word: # Very dirty. That's the hack to define the main command like create_bug. They always contains '_' for now
                    message_words.pop(index)
                else:
                    message_words.pop(index+1) # Remove the command value
                    message_words.pop(index) # Remove the command itself
        return " ".join(message_words)
    else:
        raise TypeError("Somehow there is no bot command in user message")

def get_project_from_message(message, project_command):
    """Return project from message if there was some or returns default one"""
    if project_command in message:
        message_words = message.split(" ") # Make a list of message words by spaces"
        return message_words[message_words.index(project_command)+1] # Return the next word after 'Project:' or another project command
    else:
        return 'FOT' # Default project

def get_assignee_from_message(message, assignee_command):
    """Return assignee from message if there was some or returns default one"""
    if assignee_command in message:
        message_words = message.split(" ")
        return message_words[message_words.index(assignee_command)+1] # Return the next word after 'Assignee:' or another assignee command
    else:
        return 'Anatoliy.Romsa'
