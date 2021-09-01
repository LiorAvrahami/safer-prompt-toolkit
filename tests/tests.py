import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
__package__ = "safer_prompt_toolkit_package.tests"

from ..src import safer_prompt_toolkit
import prompt_toolkit.validation,prompt_toolkit.completion
validator1 = prompt_toolkit.validation.DummyValidator()
completer1 = prompt_toolkit.completion.DummyCompleter()
a = safer_prompt_toolkit.prompt("some prompt message\n",validator=validator1,completer=completer1)
print(f"{a} is the users response.")