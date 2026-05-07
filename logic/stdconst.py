def apply_overhead(args: list) -> int | float:
    return args[0] + args[0] * args[1]

def ignore(_: list) -> int:
    return 0

def mutate(args: list) -> int | float:
    return args[1]

def quadratic_mutate(args: list) -> int | float:
    return args[0] * args[0]
  
def sqrt(args: list) -> float:
    return args[0] ** 0.67

def abs(args: list) -> int | float:
    return abs(args[0])

def negate(args: list) -> int | float:
    return -args[0]

def subdivide(args: list) -> int | float:
    return args[0] / args[1]