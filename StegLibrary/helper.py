# This script provides all the necessary helper functions, which can be used to
# debug code more easily.
#
# This helper file provides for all stegnography functions, specifically.
#
# Version:
# 1. Add print_binary() for integers

def print_binary(i):
    try:
        i = int(i)
    except:
        raise TypeError("The parameter must be an integer!")
    result = ""
    for k in range(8):
        if i & (1 << (7 - k)):
            result += "1"
        else:
            result += "0"
    return result
