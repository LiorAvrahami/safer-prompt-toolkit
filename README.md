# safer-prompt-toolkit
a wrapper to prompt-toolkit, designed to provide a fallback for some of prompt-toolkit's functionality when operating from a place where prompt-toolkit can't run.  
## intent:  
prompt-toolkit is a powerfull, command line UI, built in to almost every python interpreter. I love using it when asking the user for some input. However, prompt toolkit often complains and crashes when asked to ruin in certain non-terminal invorments (for example pycharms python console). and I find that this to be a major downside to using prompt toolkit as a minor UI part in some major project, that might somtimes be run in some context that is not the terminal.  
after making several projects that needed this functionality, and after deciding that copy pasting this prompt-toolkit fallback project is tedius and unhealthy, I desided to make this thing a project and upload it ot pypi.

## Installation
pip install safer-prompt-toolkit

## Documentation
after installing, you can import like so:
```python
import safer_prompt_toolkit
```
and you can send some prompt via:
```python
safer_prompt_toolkit.prompt("some query with validation and completion options")
```

### function documentation
#### safer_prompt_toolkit.prompt(message,max_failcase_completion_lines=3,max_chars_in_completion_line=150,**prompt_toolkit_kwargs)
use prompt_toolkit's prompt function with a fail-safe  
Parameters:  
> - message - the prompt messege to be printed to the user, (add \n at the end if you want to get the response in a new line)  
>  - max_failcase_completion_lines - defaults to 3, in case the regular prompt toolkit fails, max_failcase_completion_lines is the maximum amount of lines in the completion  
>  - max_chars_in_completion_line - defaults to 150, in case the regular prompt toolkit fails, max_chars_in_completion_line is the maximum amount of chars in a line in the completion  
>  - \*\*prompt_toolkit_kwargs - any of prompt-toolkits keywords. in case the regular prompt toolkit fails, "validator" and "completer" are used if supplied.  

info: 
> prompt_toolkit_kwargs allows you to enter some prompt_toolkit.validation.Validator instance. for example 'validator=prompt_toolkit.validation.Validator.DummyValidator()'.  
prompt_toolkit_kwargs allows you to enter some prompt_toolkit.completion.Completer instance. for example 'completer=prompt_toolkit.completion.Completer.DummyCompleter()'  

call_example:  
```python
import safer_prompt_toolkit
import prompt_toolkit.validation,prompt_toolkit.completion

validator1 = prompt_toolkit.validation.DummyValidator() # Could be any prompt_toolkit.validation.Validator instance.
completer1 = prompt_toolkit.completion.DummyCompleter() # Could be any prompt_toolkit.completion.Completer instance.

response = safer_prompt_toolkit.prompt("some prompt message\n",validator=validator1,completer=completer1)
print(f"{response} is the users response.") 
```
