def get_summary_from_message(commands: list, message):
    """Return issue summary string taken from message if there was some command at all. List of all avaluable commands are necessarry due to the 
    function return everything but the commands and their value"""
    if commands is not None:
        message_words = message.split(" ")
        summary_words_list = []
        command_word = False # Raise the flag if the next word should be the command word like Assignee: somebody"
        for index, word in enumerate(message_words):
            if command_word: # Skip the loop if the next word is the part of the command
                command_word = False
                continue
            if word in commands:
                if "_" in word: # The dirty hack for main command
                    continue
                else: # If the command like Assignee: (with two words)
                    command_word = True # Fot skipping the next word too
                    continue
            else:
                summary_words_list.append(message_words[index])
        return " ".join(summary_words_list)
    else:
        raise TypeError("Somehow there is no bot command in user message")

def get_project_from_message(message, project_command):
    """Return project from message if there was some or returns default one"""
    default_project = 'FOT'
    if project_command in message:
        message_words = message.split(" ") # Make a list of message words by spaces"
        try:
            project = message_words[message_words.index(project_command)+1] # Return the next word after 'Project:' or another project command
        except IndexError:
            return default_project
        if project != " " or "":
            return project
        else:
            return default_project
    else:
        return default_project

def get_assignee_from_message(message, assignee_command):
    """Return assignee from message if there was some or returns default one"""
    default_assignee = 'anatoliy.romsa'
    if assignee_command in message:
        message_words = message.split(" ")
        try:
            assignee = message_words[message_words.index(assignee_command)+1] # Return the next word after 'Assignee:' or another assignee command
        except IndexError:
            return default_assignee
        if assignee != " " or "": # If it's not the space
            return assignee
        else:
            return default_assignee
    else:
        return default_assignee 
