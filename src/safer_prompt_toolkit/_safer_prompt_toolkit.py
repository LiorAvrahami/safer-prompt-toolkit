import prompt_toolkit
from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completer,CompleteEvent
from prompt_toolkit.validation import Validator,ValidationError
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
import itertools

def prompt(message,max_failcase_completion_lines=3,max_chars_in_completion_line=150,**prompt_toolkit_kwargs):
    """
    :param message: the query message to write before waiting for input
    :param max_failcase_completion_lines: in case the regular prompt toolkit fails, max_failcase_completion_lines is the maximum amount of lines in the completion
    :param max_chars_in_completion_line: in case the regular prompt toolkit fails, max_chars_in_completion_line is the maximum amount of chars in a line in the completion
    :param prompt_toolkit_kwargs: any of prompt-toolkits keywords. in case the regular prompt toolkit fails, "validator" and "completer" are used if supplied.
    :return: the users response to the prompt. (a string)

    info: prompt_toolkit_kwargs allows you to enter some prompt_toolkit.validation.Validator instance, for example 'validator=prompt_toolkit.validation.DummyValidator()'.
    prompt_toolkit_kwargs allows you to enter some prompt_toolkit.completion.Completer instance, for example 'completer=prompt_toolkit.completion.DummyCompleter()'

    call_example:
    prompt("some prompt message",validator=prompt_toolkit.validation.DummyValidator(),completer=prompt_toolkit.completion.DummyCompleter())
    """
    try:
        # try using prompt toolkit
        return prompt_toolkit.prompt(message,**prompt_toolkit_kwargs)
    except NoConsoleScreenBufferError:
        # if doesn't work than try using the simplest form of input possible
        return simplest_prompt(message, max_failcase_completion_lines=max_failcase_completion_lines, max_chars_in_completion_line=max_chars_in_completion_line, **prompt_toolkit_kwargs)

def simplest_prompt(message,max_failcase_completion_lines=3,max_chars_in_completion_line=150,**prompt_toolkit_kwargs):
    validator: Validator = prompt_toolkit_kwargs["validator"] if "validator" in prompt_toolkit_kwargs else None
    completer: Completer = prompt_toolkit_kwargs["completer"] if "completer" in prompt_toolkit_kwargs else None

    while True:
        # prompt message and get answer
        user_answer = input(message)

        # validate answer
        if validator is None:
            break
        else:
            try:
                validator.validate(Document(user_answer))
                break
            except ValidationError as ve:
                print(ve.message)
                print("try again\n")

        # if invalid, offer completions
        if completer is not None:
            # astrix "*" is meant to signal completions.
            if len(user_answer) > 0 and user_answer[-1] == "*":
                user_answer = user_answer[:-1]
            # get completions
            synthetic_document = Document(user_answer, cursor_position=len(user_answer))
            completions = completer.get_completions(synthetic_document, CompleteEvent())
            print_completions(user_answer, completions, max_failcase_completion_lines, max_chars_in_completion_line,synthetic_document)
    return user_answer

def print_completions(user_answer,completions,max_failcase_completion_lines,max_chars_in_completion_line,document):
    try:
        first_completion = next(completions)
    except StopIteration:
        return

    print("---completion suggestions---")
    # loop on the first few completions and print them compactly
    completion_lines_left = max_failcase_completion_lines
    cur_completion_line = render_completion(user_answer,document,first_completion)
    for completion in completions:
        # print "max_failcase_completions_rows" number of possible completions rows

        if completion_lines_left == 0:
            print("...")
            break

        # delete from [document.cursor_position + c.start_position] to [document.cursor_position] and put c.text in it's place (c.start_position is assumed to be negative as is in prompt-toolkit)
        text = render_completion(user_answer,document,completion)# text is the current completion text

        # check if there is room in line for adding "text"
        next_possible_completion_line = cur_completion_line + " | " + text
        if len(next_possible_completion_line) > max_chars_in_completion_line:
            # if there is no more room in line, then print line, and start new line with text
            print(cur_completion_line)
            completion_lines_left -= 1
            cur_completion_line = text
        else:
            # if there is enough room in line, then then add "text" to line
            cur_completion_line = next_possible_completion_line
    if completion_lines_left > 0:
        print(cur_completion_line)
    print("----------------------------")


def render_completion(user_answer,document,completion):
    return user_answer[:document.cursor_position + completion.start_position] + completion.text + user_answer[document.cursor_position:]