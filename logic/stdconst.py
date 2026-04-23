def apply_overhead(args: list) -> int | float:
    return args[0] + args[0] * args[1]

def ignore(_: list) -> int:
    return 0

def mutate(args: list) -> int | float:
    return args[1]