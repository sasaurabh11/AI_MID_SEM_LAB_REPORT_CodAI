import random
import numpy as np
from itertools import combinations
from string import ascii_lowercase

def input_params():
    m = int(input("Enter the number of clauses in the formula: "))
    k = int(input("Enter the number of literals in a clause: "))
    n = int(input("Enter number of variables: "))
    return m, k, n

def create_problem(m, k, n):
    pos_vars = list(ascii_lowercase[:n])
    neg_vars = [var.upper() for var in pos_vars]
    all_vars = pos_vars + neg_vars
    all_combinations = list(combinations(all_vars, k))
    problems = set()
    
    while len(problems) < m:
        clause = tuple(random.sample(all_combinations, m))
        problems.add(clause)
    
    return all_vars, list(problems)

def evaluate(problem, assignment):
    return sum(any(assignment[var] for var in clause) for clause in problem)

def variable_neighborhood(problem, assignment, b, steps):
    initial_score = evaluate(problem, assignment)
    if initial_score == len(problem):
        return assignment, f"{steps}/{steps}", b

    best_assignments, scores = [], []
    
    for var in assignment.keys():
        new_assign = assignment.copy()
        new_assign[var] = 1 - new_assign[var]
        score = evaluate(problem, new_assign)
        best_assignments.append(new_assign)
        scores.append(score)
    
    selected_indices = np.argsort(scores)[-b:]
    
    if len(problem) in scores:
        idx = scores.index(len(problem))
        return best_assignments[idx], f"{steps}/{steps}", b
    
    for idx in selected_indices:
        result = variable_neighborhood(problem, best_assignments[idx], b + 1, steps + 1)
        if result:
            return result

def hill_climbing(problem, assignment, parent_score, steps):
    max_score, best_assignment = parent_score, assignment
    
    for var in assignment.keys():
        new_assign = assignment.copy()
        new_assign[var] = 1 - new_assign[var]
        score = evaluate(problem, new_assign)
        if score > max_score:
            max_score, best_assignment = score, new_assign
            steps += 1
            
    if max_score == parent_score:
        return assignment, max_score, f"{steps}/{steps - len(assignment)}"
    
    return hill_climbing(problem, best_assignment, max_score, steps)

def beam_search(problem, assignment, b, step_size):
    initial_score = evaluate(problem, assignment)
    if initial_score == len(problem):
        return assignment, f"{step_size}/{step_size}"
    
    best_assignments, scores = [], []
    
    for var in assignment.keys():
        new_assign = assignment.copy()
        new_assign[var] = 1 - new_assign[var]
        score = evaluate(problem, new_assign)
        best_assignments.append(new_assign)
        scores.append(score)
    
    selected_indices = np.argsort(scores)[-b:]
    
    if len(problem) in scores:
        idx = scores.index(len(problem))
        return best_assignments[idx], f"{step_size}/{step_size}"
    
    for idx in selected_indices:
        result = beam_search(problem, best_assignments[idx], b, step_size + 1)
        if result:
            return result

def random_assignment(variables, n):
    assignment = np.random.choice([0, 1], size=n).tolist()
    return dict(zip(variables, assignment + [1 - val for val in assignment]))

def main():
    m, k, n = input_params()
    variables, problems = create_problem(m, k, n)
    
    results = []
    
    for i, problem in enumerate(problems, 1):
        assignment = random_assignment(variables, n)
        initial_score = evaluate(problem, assignment)
        
        hill_result = hill_climbing(problem, assignment, initial_score, 1)
        beam_result_3 = beam_search(problem, assignment, 3, 1)
        beam_result_4 = beam_search(problem, assignment, 4, 1)
        variable_result = variable_neighborhood(problem, assignment, 1, 1)
        
        results.append((i, problem, hill_result, beam_result_3, beam_result_4, variable_result))

    print("\n" + "=" * 50 + "\n")
    print("Results Summary:")
    print("-" * 50)
    
    for result in results:
        i, problem, hill_result, beam_result_3, beam_result_4, variable_result = result
        
        print(f"Problem {i}: {problem}")
        print(f"{'-' * 50}")
        print(f"Hill Climbing Solution: {hill_result[0]}")
        print(f"  - Score: {evaluate(problem, hill_result[0])}")
        print(f"  - Penetration: {hill_result[2]}")
        print()
        
        print(f"Beam Search (b=3) Solution: {beam_result_3[0]}")
        print(f"  - Score: {evaluate(problem, beam_result_3[0])}")
        print(f"  - Penetration: {beam_result_3[1]}")
        print()
        
        print(f"Beam Search (b=4) Solution: {beam_result_4[0]}")
        print(f"  - Score: {evaluate(problem, beam_result_4[0])}")
        print(f"  - Penetration: {beam_result_4[1]}")
        print()
        
        print(f"Variable Neighborhood Solution: {variable_result[0]}")
        print(f"  - Score: {evaluate(problem, variable_result[0])}")
        print(f"  - Penetration: {variable_result[1]}")
        print()
        print("=" * 50)

if __name__ == "__main__":
    main()
