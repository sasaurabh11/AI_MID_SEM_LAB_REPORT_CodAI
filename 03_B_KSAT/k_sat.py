from string import ascii_lowercase
import random
from itertools import combinations
from typing import List, Tuple

def inputs() -> Tuple[int, int, int]:
    m = int(input("Enter the number of clauses required: "))
    k = int(input("Enter the number of variables in a clause: "))
    n = int(input("Enter the number of variables: "))
    return m, k, n

def gen_vars(n: int) -> List[str]:
    positive_vars = list(ascii_lowercase)[:n]
    negative_vars = [var.upper() for var in positive_vars]
    return positive_vars + negative_vars

def gen_comb(variables: List[str], k: int) -> List[Tuple[str]]:
    return list(combinations(variables, k))

def make_problem(m: int, k: int, n: int) -> List[List[List[str]]]:
    variables = gen_vars(n)
    all_combinations = gen_comb(variables, k)
    unique_problems = set()

    while len(unique_problems) < m:
        selected_combinations = random.sample(all_combinations, m)
        unique_problems.add(tuple(selected_combinations))

    return [list(problem) for problem in unique_problems]

def print_p(problems: List[List[List[str]]]) -> None:
    for problem in problems:
        for clause in problem:
            print(clause)
        print()

def main() -> None:
    m, k, n = inputs()
    problems = make_problem(m, k, n)
    print_p(problems)

if __name__ == "__main__":
    main()
