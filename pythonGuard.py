# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 16:07:24 2013

@author: Evan Manuella
@description: Guard Procedures for the Python GimpDBus client
"""

# This library differs significantly from its racket counter part.
# The types are checked within each procedure, eliminating the need
# for external procedures to check. Whatever was not checked within 
# the original wrapper, I wrote here.

import inspect

### Procedure:      error_arrity
###
### Parameters:     func: the function which will be checked
###                 given_args: the arguments which will be checked
###                 against the function's expected arguments
###
### Purpose:        to check for and deal with an arrity mistake
###
### Produces:       True, if expected number of args equals the given number of args
###                 A string to be given to the user, which describes the descrepancy
###
### Preconditions:  [No additional]
###
### Postconditions: [No additional]


def error_arrity(func, given_args):
    args = inspect.getargspec(func)
    leng_expected = len(args[0])
    leng_given = len(given_args)
    if leng_expected != leng_given:
        output = 'Error: expected '
        if leng_expected == 1:
            output += '1 argument, given'
        else:
            output += str(leng_expected)
            output += ' arguments, given '
        output += str(leng_given)
        output += '\n'
        return output
    return True


