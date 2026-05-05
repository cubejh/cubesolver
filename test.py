import time
from solver.mainsolver import CubeSolver
"""
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
"""

start_time = time.time()
cubesolver = CubeSolver()
solution = cubesolver.solve_scramble("B' L' B2 R2 F2 L' D2 R U2 R2 U2 R' B' R U' L U2 L' D2 B'")
solve_time = time.time()-start_time
print(f"==========\nSolve Time: {solve_time:.4f}\n==========")