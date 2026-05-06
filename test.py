import time
from solver.mainsolver import CubeSolver

if __name__ == '__main__': 
    start_time = time.time()
    cubesolver = CubeSolver()
    solution_p1 = cubesolver.solve_piece_def("LERPOUNSAIMG","WFEPSLNJ")
    #solution = cubesolver.solve_scramble("B' L' B2 R2 F2 L' D2 R U2 R2 U2 R' B' R U' L U2 L' D2 B'")
    solve_time = time.time()-start_time
    print(f"==========\nSolve Time: {solve_time:.4f}\n==========")