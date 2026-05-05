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
solution = cubesolver.solve_scramble("R2 D2 R2 F' L2 B' L2 F2 L2 R2 U' F' U2 F L B2 U2 L'")
solution = cubesolver.solve_scramble("B2 L2 B2 R2 D2 F L2 F2 U2 F' U2 R' D U' F L R2 F2 R B' U2")
solution = cubesolver.solve_scramble("R2 F2 R' U' F B' D L' D' R' U2 F2 U2 F2 R' U2 R' U2 L2 D2 L'")
solution = cubesolver.solve_scramble("F2 U L2 U' R2 B2 D F2 R2 D2 F2 U' L D' B2 D L' B2 F' D R2")
solve_time = time.time()-start_time
print(f"==========\nSolve Time: {solve_time:.4f}\n==========")