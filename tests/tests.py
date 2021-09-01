import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
__package__ = "safer_prompt_toolkit_package.tests"

from ..src import safer_prompt_toolkit
safer_prompt_toolkit.prompt("lior")
