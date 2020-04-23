import pytest
from bot_command_parser import get_summary_from_message, get_project_from_message, get_assignee_from_message

@pytest.mark.parametrize("test_message, test_cmd_list, expected", 
        [
            ("create_bug Fix some value within the field", ["create_bug", "Assignee:"], "Fix some value within the field"), 
            ("create_improvement Summary of the issue Project: Assignee:", ["create_improvement", "Project:", "Assignee:"], "Summary of the issue")
            ])
def test_get_summary_from_message(test_message, test_cmd_list, expected):
    assert get_summary_from_message(test_cmd_list, test_message) == expected

def test_error_get_summary_from_message():
    try:
        result = get_summary_from_message([], "some message without command")
    except(TypeError):
        assert(True)

@pytest.mark.parametrize("test_msg, test_cmd, expected", 
        [
            ("create_story Some story Project: BRU Assignee: anatoliy.anatoliy", "Project:", "BRU"), 
            ("create_task Some stru without project Assignee: test.test", "Project:", "FOT")
            ])
def test_get_project_from_message(test_msg, test_cmd, expected):
    assert get_project_from_message(test_msg, test_cmd) == expected

@pytest.mark.parametrize("test_msg, test_cmd, expected", 
        [
            ("create_improvement Some impr of the issue Assignee: test.test", "Assignee:", "test.test"), 
            ("create_bug Some bug Project: FOT Assignee: me", "Assignee:", "me"), 
            ("create_bug Find some beer", "Assignee:", "Anatoliy.Romsa")
            ])
def test_get_assignee_from_message(test_msg, test_cmd, expected):
    assert get_assignee_from_message(test_msg, test_cmd) == expected
