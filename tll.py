"""A tiny little language in one file."""

import json
import sys


def do_add(env, args):
    """Add two values.

    ["add" A B] => A + B
    """
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1]) # do to get variable
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

    ["neg" A] => -A
    """
    assert len(args) == 1
    return -do(env, args[0])


def do_not(env, args):
    """Logical negation.

    ["not" A] => not A
    """
    assert len(args) == 1
    # should new language check args type (bool)
    return not do(env, args[0])


def do_or(env, args):
    """Logical or.
    The second sub-expression is only evaluated if the first is false.

    ["or" A B] => A or B
    """
    assert len(args) == 2
    # @here: case where temp := doesn't assign?
    # If temp is False (args[0]) then return args[1] 
    if temp := do(env, args[0]):
        return temp
    return do(env, args[1])


def do_print(env, args):
    """Print values.

    ["print" ...values...] => None # print each value
    """
    args = [do(env, a) for a in args]
    # * unpacks the list
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

# new repeat with counter
def do_repeat_count(env, args):
    """Repeat instructions some number of times.
    but now counter is accessible
    ["repeat" N n_name expr] => expr # last one of N

    ## but what if want to modify it -> not a good idea just question
    """
    assert len(args) == 3
    count = do(env, args[0])
    for i in range(count):
        do_set(env, args[1], i)
        result = do(env, args[2])
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

    ["seq" name expr] => expr # and env{name} = expr
    """
    assert len(args) == 2
    assert isinstance(args[0], str)
    value = do(env, args[1])
    env[args[0]] = value
    return value


def do_array(env,args):
    """ 
    Make a fixed length array 


    ["array", "new", 10]
    # How do we really initialize something
    # what if not fixed - just change env variable? @here
    # what if variable have the same name - same key
    # How can programmers catch all exceptions there is (also repeating tests?)
    """
    name_arr = args[0]
    num_ele = args[1]
    assert isinstance(args[0],str)
    assert int(num_ele) >= 0
    env[name_arr]=[0]*num_ele # initialize as 0?

def do_set_array(env,args):
    """
    Set particular element in array
    name of array, index and new value
    ["set_array" name indx new_value]
    """
    assert len(args) == 3
    assert args[0] in env.keys()
    assert isinstance(args[1],int)
    assert args[1] >= 0
    assert len(env[args[0]]) >= args[1]-1
    original_lst = env[args[0]]
    new_lst = env[args[0]]
    new_lst[args[1]] = args[2]
    env[args[0]] = new_lst

def do_get_array(env,args):
    """
    get particular element in array
    name of array, index
    ["get_array" name 0]
    """
    assert args[0] in env.keys()
    assert isinstance(args[1],int)
    assert args[1] >= 0
    assert len(env[args[0]]) >= args[1]-1
    return env[args[0]][args[1]]

"""
Q2: while
"""
def do_while(env,args):
    """
    while loop (if satisfy condition then end)
    ["while" C expr]

    # Any problem using recursion?
    """
    assert len(args) == 2
    
    if not args[0]:
        do(env, args[1])
    if not args[0]:    
        do_while(env, args)


# Lookup table of operations.
OPERATIONS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}
"""
Q4: 
- Operations table is a dictionary of functions here (that start with `do_`)
- Local scope = within a function & class; Global includes name, main, doc etc
- The function is stored in the dictionary as items, key being the name (stripped of `do_`)
- This allows the do function to look up which function and pass it to that

# Same function name - from same or different package?
# Change function in the middle - would need to update
"""

def do(env, instruction):
    """Run the given instruction in the given environments."""
    if not isinstance(instruction, list):
        return instruction
    op, args = instruction[0], instruction[1:]
    assert op in OPERATIONS
    return OPERATIONS[op](env, args)


if __name__ == "__main__":
    program = json.load(sys.stdin)
    result = do({}, program)
    print("=>", result)

"""
Q5. Exceptions

# Should this be child class of Exception?
# better to construct one class than multiple for different kinds of errors?
# Also why not just annotate the assertions - for better info?
"""
class TLLExceptions(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def check(script_path):
        try:
            program = json.load(sys.stdin)
            result = do({},program)
        except:
            raise TLLExceptions("Error in code")
