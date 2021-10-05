import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
__package__ = "safer_prompt_toolkit_package.tests"

from ..src import safer_prompt_toolkit
import prompt_toolkit.validation,prompt_toolkit.completion
completer1,validator1 = safer_prompt_toolkit.make_ConstantOptions_Completer_and_Validator(["option1","option2","banana","option3"],preferred_option="banana")
a = safer_prompt_toolkit.prompt("some prompt message\n",validator=validator1,completer=completer1)
print(f"{a} is the users response.")

a = safer_prompt_toolkit.prompt("some prompt message\n",
                                **safer_prompt_toolkit.make_ConstantOptions_Completer_and_Validator__return_kwargs(iter(["option1","option2","banana","option3"]),preferred_option="banana"))
print(f"{a} is the users response.")