import time
from solver.mainsolver import CubeSolver

if __name__ == '__main__': 
    cubesolver = CubeSolver()
    start_time = time.time()
    cubesolver.solve_scramble("B' L' B2 R2 F2 L' D2 R U2 R2 U2 R' B' R U' L U2 L' D2 B'")
    solve_time = time.time()-start_time
    print(f"==========\nSolve Time: {solve_time:.4f}\n==========")

    try:
        print("From Piece_def(full):")
        cubesolver.solve_piece_def("IKXFSVPREBAT","SQDGVATM")
    except Exception as e :
        print("error:", e)

    print("From Piece_def:")
    cubesolver.solve_piece_def_p1("KIXFSVPREBAT","SQDGVATM")
    print("==========\nFrom Piece_orientation_def:")
    cubesolver.solve_piece_orientation_def_p1("U1C1X0L1W1V0J1R0D1B0A0T0","X2B2D0U2V0A0W1C2")