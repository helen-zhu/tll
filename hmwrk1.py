"""Homework 1"""

import json
import sys

# Question 1: Array
def do_array(env, args):
    """Generates an array of length args[1]
    Question - what happens when args[0] is not new?
    ["array" "new" 10] -> creates an array of length 10
    """
    assert len(args) == 2
    assert isinstance(args[0], str)
    assert isinstance(args[1], int)
    if args[0] == "new":
        return [None]*args[1]

def do_set_element(env, args):
    """Sets an element in an array to a specific value
    ["set_element" array_name 0 1] -> sets array_name[0] = 1
    """
    assert len(args) == 3
    assert args[0] in env, f"Unknown variable {args[0]}"
    assert isinstance(env[args[0]], list)
    assert isinstance(args[1], int)
    assert args[1] < len(env[args[0]])
    value = do(env, args[2])
    env[args[0]][args[1]] = value
    return value

def do_retrieve_element(env, args):
    """Retrieves element of index
    ["retrieve_element" array_name 0] -> retrieves array_name[0]
    """
    assert len(args) == 2
    assert args[0] in env, f"Unknown variable {args[0]}"
    assert isinstance(env[args[0]], list)
    assert isinstance(args[1], int)
    assert args[1] < len(env[args[0]])
    return env[args[0]][args[1]]

# While
def do_while(env, args):
    """Repeats an action while a statement remains true
    ["while" condition action]
    *** What is this supposed to return?
    """
    assert len(args) == 2
    cond = do(env, args[0])
    if cond:
        do(env, args[1])
        do_while(env, args)
    return None

# New repeat
def do_repeat(env, args):
    """Repeat instructions some number of times.

    ["repeat" N expr] => expr # last one of N

    *** setting a global variable called count to i
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        do_set(env, ["count", i])
        result = do(env, args[1])
    return result

# Writing a TLL exception class
class TLLException(Exception):
    """Exception raised when there's a problem
    """
    def __init__(self, message = "ERROR: Please revise!"):
        self.message = message
        super().__init__(self.message)

def check:
    pass

# Rewriting docstrings for do_repeat and do_seq
def do_repeat(env, args):
    """Repeat one operation N times

    ["repeat" N expr] => expr # last one of N
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result


def do_seq(env, args):
    """Execute a list of operations sequentially

    ["seq" A B...] => last expr # execute in order
    """
    for a in args:
        result = do(env, a)
    return result
