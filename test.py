import time
from solver.mainsolver import full_solver

start_time = time.time()
solution = full_solver("R' U' F U2 F R2 B2 F2 D' R2 D' L2 D L2 R2 F2 B' R' U L2 D2 R U' B' R' U' F")
solution = full_solver("R' U' F D2 U2 B2 R U2 F2 R D2 B2 L B' F D' B2 R D2 L' B D' B2 R' U' F")
solution = full_solver("R' U' F U R' F2 U' L' D' B L D' U2 L2 B' R2 B D2 F2 L2 D2 L2 U2 B2 R' U' F")
solution = full_solver("R' U' F D2 L B L2 B' F L2 R2 F' U2 L2 R2 U' R' U2 L2 D' R2 F' D2 R' U' F")
solve_time = time.time()-start_time
print(f"==========\nSolve Time: {solve_time:.4f}\n==========")