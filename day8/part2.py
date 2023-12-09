import pathlib
import os
from math import lcm
from modint import chinese_remainder

THIS_DIR = pathlib.Path(__file__).parent.resolve()
from functools import reduce
def chinese_remainder_bad(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def find_loop(start, ends, graph, instructions):
    seen = set()
    steps = 0
    curr = (start, 0)
    while curr not in seen:
        seen.add(curr)
        mod_steps = steps % len(instructions)
        if instructions[mod_steps] == "L":
            curr = (graph[curr[0]][0], mod_steps)
        else:
            curr = (graph[curr[0]][1], mod_steps)
        steps += 1
    loop_size = 0
    lcurr = curr
    loop_ends = []
    while loop_size == 0 or lcurr != curr:
        mod_steps = (steps + loop_size) % len(instructions)
        if lcurr[0] in ends:
            loop_ends.append(steps + loop_size)
        if instructions[mod_steps] == "L":
            lcurr = (graph[lcurr[0]][0], mod_steps)
        else:
            lcurr = (graph[lcurr[0]][1], mod_steps)
        loop_size += 1
    return loop_size, loop_ends[0]


# Copied from https://math.stackexchange.com/a/3864593
def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

        The combined rotation is at its reference point if and only if both a and b
            are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
     gcd: The greatest common divisor of a and b
     s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def find_min(starts, ends, graph, instructions):
    loops = [find_loop(start, ends, graph, instructions) for start in starts]
    phase, period = loops[0][1], loops[0][0]
    for loop in loops[1:]:
        period, phase = combine_phased_rotations(period, phase, loop[1], loop[0])

    return -phase % period

with open(os.path.join(THIS_DIR, "input.txt")) as f:
    lines = f.readlines()
    instructions = lines[0].strip()

    graph = {}
    for line in lines[2:]:
        s, to = line.strip().split(" = ")
        l, r = to[1:-1].split(", ")
        graph[s] = (l, r)

starts = {s for s in graph.keys() if s.endswith("A")}
ends = {s for s in graph.keys() if s.endswith("Z")}
print(lcm(*[find_loop(start, ends, graph, instructions)[1]//2 for start in starts]))
print(find_min(starts, ends, graph, instructions))