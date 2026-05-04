import os
import time
from cube import Cube
from notation import parse_moves  # 假設你的 Move 和 parse_moves 在 notation.py
from p1_table import TableManager

def test_with_scramble():
    print("=== Phase 1 Distance Test with Scramble String ===")

    # 1. 初始化 TableManager (自動載入或建表)
    start_time = time.time()
    tm = TableManager(folder="cube_data")
    print(f"System initialized in {time.time() - start_time:.2f}s")

    # 2. 準備方塊與打亂字串
    cube = Cube.newcube()
    scramble_str = "R' L B' D2 L2 B2 L' D R' L2 F2 B2 D R2 U' D' L2 F2 D' R2"
    
    print(f"\n[Scramble]: {scramble_str}")
    
    # 3. 解析並執行動作
    moves = parse_moves(scramble_str)
    for m in moves:
        m.apply(cube)
    
    # 4. 獲取距離
    dist = tm.get_distance(cube)
    print(f"\n[Result] Distance to Phase 2: {dist} moves")
    
    # 5. 驗證是否能回到 0 (手動執行一個反向測試)
    # 這裡我們用一個簡單的字串來測試還原邏輯
    print("\n--- Verification: Simple Move & Undo ---")
    test_cube = Cube.newcube()
    test_moves = parse_moves("U R F'")
    
    print("Applying U R F'...")
    for m in test_moves:
        m.apply(test_cube)
    print(f"Distance: {tm.get_distance(test_cube)}")

    # 這裡示範如何手動反向旋轉
    # U R F' 的反向是 F R' U'
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
    # 如果你更換了 DistanceTable 邏輯，請記得先刪除舊的 .bin 檔案再執行
    test_with_scramble()