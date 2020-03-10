from scpython.options import Branch, Language
import re


def getScpBranch(code):
    """Detects an SCP's branch by its code.

    Args:
        code (str): The SCP's code.

    Return:
        (scpython.options.Branch): The SCP's branch.
    """
    languages = [l.name for l in list(Branch)]
    regex = f"-({'|'.join(languages)})"

    ret = Branch.EN
    match = re.search(regex, code)
    if match:
        b = match.group(1)
        ret = getItemByName(Branch, b)
    return ret


def getItemByName(enum, name):
    """Gets an enum item by its variable name.

    Args:
        enum (Enum): The enum to check.
        name (str): The name of the variable to find.

    Return:
        The enum variable, or None.
    """
    for x in list(enum):
        if x.name == name:
            return x
    return None
