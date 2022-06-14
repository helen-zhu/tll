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

# Rewriting docstrings for do_repeat and do_seq
# def do_repeat(env, args):
#     """Repeat one operation N times
#
#     ["repeat" N expr] => expr # last one of N
#     """
#     assert len(args) == 2
#     count = do(env, args[0])
#     for i in range(count):
#         result = do(env, args[1])
#     return result


def do_seq(env, args):
    """Execute a list of operations sequentially

    ["seq" A B...] => last expr # execute in order
    """
    for a in args:
        result = do(env, a)
    return result

def do_add(env, args):
    """Add two values.

    ["add" A B] => A + B
    """
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_comment(env, args):
    """Ignore instructions.

    ["comment" "text"] => None
    """
    return None


def do_get(env, args):
    """Get the value of a variable.

    ["get" name] => env{name}
    """
    assert len(args) == 1
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]


def do_gt(env, args):
    """Strictly greater than.

    ["gt" A B] => A > B
    """
    assert len(args) == 2
    return do(env, args[0]) > do(env, args[1])


def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.

    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)


def do_leq(env, args):
    """Less than or equal.

    ["leq" A B] => A <= B
    """
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])


def do_neg(env, args):
    """Arithmetic negation.

    ["neq" A] => -A
    """
    assert len(args) == 1
    return -do(env, args[0])


def do_not(env, args):
    """Logical negation.

    ["not" A] => not A
    """
    assert len(args) == 1
    return not do(env, args[0])


def do_or(env, args):
    """Logical or.
    The second sub-expression is only evaluated if the first is false.

    ["or" A B] => A or B
    """
    assert len(args) == 2
    if temp := do(env, args[0]):
        return temp
    return do(env, args[1])


def do_print(env, args):
    """Print values.

    ["print" ...values...] => None # print each value
    """
    args = [do(env, a) for a in args]
    print(*args)
    return None


def do_repeat(env, args):
    """Repeat instructions some number of times.

    ["repeat" N expr] => expr # last one of N
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result


def do_seq(env, args):
    """Do a sequence of operations.

    ["seq" A B...] => last expr # execute in order
    """
    for a in args:
        result = do(env, a)
    return result


def do_set(env, args):
    """Assign to a variable.

    ["set" name expr] => expr # and env{name} = expr

    *** Why does this return value?
    """
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value


# Lookup table of operations.
OPERATIONS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}


def do(env, instruction):
    """Run the given instruction in the given environments."""
    if not isinstance(instruction, list):
        return instruction
    op, args = instruction[0], instruction[1:]
    assert op in OPERATIONS
    return OPERATIONS[op](env, args)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as reader:
            program = json.load(reader)
    else:
        program = json.load(sys.stdin)
    result = do({}, program)
    print("=>", result)
