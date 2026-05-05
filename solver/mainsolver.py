import os
import time
from core.cube import Cube
from core.notation import parse_moves, from_piece_def_init, from_piece_orient_init
from tables.p1_table import TableManager
from tables.p2_table import TableManagerP2
from solver.phase1solver import Phase1Solver
from solver.phase2solver import Phase2Solver

def test_with_phase1solver(scramble):
    start_time = time.time()
    tm = TableManager(folder="cube_data")
    solver = Phase1Solver(tm)
    cube = Cube.newcube()
    
    for m in parse_moves(scramble):
        m.apply(cube)

    print(f"Scramble: {scramble}")
    solution = solver.solve(cube)
    solve_time = time.time() - start_time
    print(f"Solve Time: {solve_time:.4f} seconds\n")

    #edge_string = "OCXLWKEHNPAB"
    #corner_string = "CLIXPRBT"
    #print(f"edge_string: {edge_string}")
    #print(f"corner_string: {corner_string}")
    #cube2 = from_piece_def_init(edge_string, corner_string)
    #solver.solve(cube2)

def full_solver(scramble):
    tm1 = TableManager(folder="cube_data")
    solver1 = Phase1Solver(tm1)
    
    tm2 = TableManagerP2(folder="cube_data")
    solver2 = Phase2Solver(tm2)

    cube = Cube.newcube()
    scramble_moves = parse_moves(scramble)
    for m in scramble_moves:
        m.apply(cube)

    print(f"Scramble: {scramble}")

    solution1 = solver1.solve(cube)
    
    if solution1:
        p1_moves = parse_moves(solution1)
        for m in p1_moves:
            m.apply(cube)

        solution2 = solver2.solve(cube)
    else:
        solution2 = None

    if solution1 and solution2:
        full_solution = f"{solution1} {solution2}".strip()
        full_solution = simplify_moves(full_solution)
        print(f"Full Solution: {full_solution}")
        print(f"Steps: {len(full_solution.split())}")
    else:
        print("Failed to find a complete solution.")
    return full_solution

def simplify_moves(move_str):
    if not move_str:
        return ""
    
    moves = move_str.split()
    simplified = []
    
    for move in moves:
        face = move[0]
        if len(move) == 1:
            amount = 1
        elif move[1] == '2':
            amount = 2
        elif move[1] == "'":
            amount = 3
        else:
            amount = 1

        if simplified and simplified[-1][0] == face:
            prev_face, prev_amount = simplified.pop()
            new_amount = (prev_amount + amount) % 4
            
            if new_amount != 0:
                simplified.append((prev_face, new_amount))
        else:
            simplified.append((face, amount))
    
    res = []
    for f, a in simplified:
        if a == 1: res.append(f)
        elif a == 2: res.append(f + "2")
        elif a == 3: res.append(f + "'")
        
    return " ".join(res)