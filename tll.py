"""A tiny little language in one file."""

import json
import sys


def do_add(env, args):
    """Add two values."""
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_comment(env, args):
    """Ignore instructions."""
    return None


def do_get(env, args):
    """Get the value of a variable."""
    assert len(args) == 1
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]


def do_gt(env, args):
    """Strictly greater than."""
    assert len(args) == 2
    return do(env, args[0]) > do(env, args[1])


def do_if(env, args):
    """Make a choice."""
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)


def do_leq(env, args):
    """Less than or equal."""
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])


def do_neg(env, args):
    """Arithmetic negation."""
    assert len(args) == 1
    return -do(env, args[0])


def do_not(env, args):
    """Logical negation."""
    assert len(args) == 1
    return not do(env, args[0])


def do_or(env, args):
    """Logical or."""
    assert len(args) == 2
    if temp := do(env, args[0]):
        return temp
    return do(env, args[1])


def do_print(env, args):
    """Print values."""
    args = [do(env, a) for a in args]
    print(*args)
    return None


def do_repeat(env, args):
    """Repeat instructions some number of times."""
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result


def do_seq(env, args):
    """Do a sequence of operations."""
    for a in args:
        result = do(env, a)
    return result


def do_set(env, args):
    """Assign to a variable."""
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
    program = json.load(sys.stdin)
    result = do({}, program)
    print("=>", result)
