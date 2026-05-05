import os
import time
from core.cube import Cube
from core.notation import parse_moves, from_piece_def_init, from_piece_orient_init
from tables.p1_table import TableManager
from solver.phase1solver import Phase1Solver

def test_with_phase1solver(scramble):
    tm = TableManager(folder="cube_data")
    solver = Phase1Solver(tm)

    cube = Cube.newcube()
    print(f"Scrambling with: {scramble}")
    for m in parse_moves(scramble):
        m.apply(cube)
    solver.solve(cube)

    edge_string = "OCXLWKEHNPAB"
    corner_string = "CLIXPRBT"
    print(f"edge_string: {edge_string}")
    print(f"corner_string: {corner_string}")
    cube2 = from_piece_def_init(edge_string, corner_string)
    solver.solve(cube2)


def test_with_scramble():
    print("=== Phase 1 Distance Test with Scramble String ===")

    # 1. 初始化 TableManager (自動載入或建表)
    start_time = time.time()
    tm = TableManager(folder="cube_data")
    print(f"System initialized in {time.time() - start_time:.2f}s")
    
    print("\n--- Verification: Simple Move & Undo ---")
    test_cube = Cube.newcube()
    test_moves = parse_moves("U R F'")
    
    print("Applying U R F'...")
    for m in test_moves:
        m.apply(test_cube)
    print(f"Distance: {tm.get_distance(test_cube)}")

    undo_moves = parse_moves("F R' U'")
    print("Applying Undo moves (F R' U')...")
    for m in undo_moves:
        m.apply(test_cube)
    
    final_dist = tm.get_distance(test_cube)
    print(f"Final Distance: {final_dist} (Expected: 0)")

    if final_dist == 0:
        print("\n✅ Verification SUCCESS!")
    else:
        print("\n❌ Verification FAILED!")

if __name__ == "__main__":
    test_with_scramble()
    print("===================")
    test_with_phase1solver("R2 U' F2 D' U2 R2 U L2 B2 U L D' B U F' U' B' R2 B' F")