"""
Utilities for boolean operations

...

Methods
-------
str_to_bool(s)
    Converts string to boolean
"""


def str_to_bool(s):
    """
    Converts string to boolean

    Python 'bool' built-in method has a different conception of use

    Parameters
    ----------
    s : str
        string to be converted

    Returns
    -------
    bool
        converted bool

    Raises
    ------
    ValueError
        if value is not a boolean value
    """
    
    if type(s) == str:
        b = s.lower()
        if b == 'true':
            return True
        elif b == 'false':
            return False
    elif type(s) == bool:
        return s
    else:
         raise ValueError
