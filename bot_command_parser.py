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
        
def get_case_insensetive_command_value(message_list: list, command: str) -> str:
    """Return the value of command despite the used cased if the command really exists or None if the list or command are None"""
    if message_list and command is not None:
        try:
            command_value = message_list[message_list.index(command)+1]
        except ValueError:
            command_value = message_list[message_list.index(command.lower())+1]
        except IndexError:
            command_value = None
        return command_value
    return None

def get_project_from_message(message, project_command):
    """Return project from message if there was some or returns default one"""
    default_project = 'FOT'
    if project_command.lower() in message.lower():
        message_words = message.split(" ") # Make a list of message words by spaces"
        project = get_case_insensetive_command_value(message_words, project_command)
        if project is not None:
            if project != "" and project != " ":
                return project
    return default_project

def get_assignee_from_message(message, assignee_command):
    """Return assignee from message if there was some or returns default one"""
    default_assignee = 'anatoliy.romsa'
    if assignee_command.lower() in message.lower():
        message_words = message.split(" ")
        assignee = get_case_insensetive_command_value(message_words, assignee_command)
        if assignee is not None:
            if assignee != "" and assignee != " ":
                return assignee
    return default_assignee

def get_priority_from_message(message, priority_command):
    """ Returns priority from message. Otherwise returns 'P3'"""
    default_priority = "P3"
    if priority_command.lower() in message.lower():
        message_words = message.split(" ")
        priority = get_case_insensetive_command_value(message_words, priority_command)
        if priority is not None:
            if priority != "" and priority != " ":
                return priority
    return default_priority
