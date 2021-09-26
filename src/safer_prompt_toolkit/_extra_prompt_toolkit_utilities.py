from typing import Iterable
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator,ValidationError
from prompt_toolkit.completion import Completer, Completion, CompleteEvent


def make_ConstantOptions_Completer_and_Validator(options, preferred_option=None, preferred_option_styles=["bg:ansibrightgreen fg:ansiblack","bg:ansigreen fg:ansiwhite"], b_complete_only_if_requested = False):
        return ConstantOptionsCompleter(options,preferred_option,preferred_option_styles,b_complete_only_if_requested),\
               ConstantOptionsValidator(options)


class ConstantOptionsCompleter(Completer):
    def __init__(self, options, preferred_option=None, preferred_option_styles=["bg:ansibrightgreen fg:ansiblack","bg:ansigreen fg:ansiwhite"], b_complete_only_if_requested = False):
        self.options = options
        self.b_complete_only_if_requested = b_complete_only_if_requested
        self.preferred_option = preferred_option
        self.preferred_option_styles = preferred_option_styles

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        if complete_event.completion_requested or not self.b_complete_only_if_requested:
            for o in self.options:
                if o == self.preferred_option:
                    yield Completion(o, -document.cursor_position, style=self.preferred_option_styles[0], selected_style=self.preferred_option_styles[1])
                else:
                    yield Completion(o, -document.cursor_position)
        return []


class ConstantOptionsValidator(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, document: Document) -> None:
        if document.text not in self.options:
            raise ValidationError(cursor_position=0,message="invalid submission, press tab to see your options")