import os
from collections import deque
import time
from core.cube import Cube
from tables.move_table_manager_p1 import MoveTableManager
from tables.distance_table import DistanceTable

class TableManager:
    def __init__(self, folder="tables"):
        self.folder = folder
        self.FS_SIZE = (2**11) * 495
        self.TS_SIZE = (3**7) * 495
        self.num_moves = 18

        self.moves = [(f, a) for f in ['U', 'D', 'R', 'L', 'F', 'B'] for a in [0, 1, 2]]
        self.num_moves = len(self.moves)

        # 1. Initialize/Load Move Tables
        move_mgr = MoveTableManager(folder)
        self.fs_move, self.ts_move = move_mgr.build_or_load_move_tables()

        # 2. Initialize Pruning Tables (using DistanceTable)
        self.fs_table = DistanceTable(self.FS_SIZE)
        self.ts_table = DistanceTable(self.TS_SIZE)
        self.load_or_build_pruning()

    def load_or_build_pruning(self):
        fs_path = os.path.join(self.folder, "fs_pruning.bin")
        ts_path = os.path.join(self.folder, "ts_pruning.bin")

        if os.path.exists(fs_path) and os.path.exists(ts_path):
            print("--- Loading pruning tables from disk ---")
            self.fs_table = DistanceTable.from_file(fs_path)
            self.ts_table = DistanceTable.from_file(ts_path)
            print("Pruning tables loaded successfully.")
        else:
            print("--- Starting Pruning Table Generation ---")
            total_start = time.time()
            
            # 保留你原始的起點定義邏輯
            start_cube = Cube.newcube()
            start_fs = start_cube.get_flip_slice_val()
            start_ts = start_cube.get_twist_slice_val()

            # 1. Flip-Slice
            print(f"\nBuilding Flip-Slice Pruning Table (Size: {self.FS_SIZE})...")
            fs_start = time.time()
            self._build_pruning_table(self.fs_table, self.fs_move, start_fs, "Flip-Slice")
            self.fs_table.to_file(fs_path)
            fs_end = time.time()
            print(f"Finished.")
            print(f"  - Time taken: {fs_end - fs_start:.2f} seconds")
            
            # 2. Twist-Slice
            print(f"\nBuilding Twist-Slice Pruning Table (Size: {self.TS_SIZE})...")
            ts_start = time.time()
            self._build_pruning_table(self.ts_table, self.ts_move, start_ts, "Twist-Slice")
            self.ts_table.to_file(ts_path)
            ts_end = time.time()
            print(f"Finished.")
            print(f"  - Time taken: {ts_end - ts_start:.2f} seconds")

            total_end = time.time()
            print(f"\n{'='*50}")
            print(f"Pruning tables built and saved in {total_end - total_start:.2f} seconds.")
            print(f"{'='*50}")

    def _build_pruning_table(self, pruning_table, move_table, start_val, name):
        """完全保留你原本的 BFS 邏輯"""
        pruning_table.set(start_val, 0)
        queue = deque([start_val])
        visited_count = 1
        
        while queue:
            curr_val = queue.popleft()
            curr_dist = pruning_table.get(curr_val)
            next_dist = curr_dist + 1

            for move_idx in range(self.num_moves):
                child_val = move_table[curr_val * self.num_moves + move_idx]
                
                if child_val != -1 and pruning_table.get(child_val) == 255:
                    pruning_table.set(child_val, next_dist)
                    queue.append(child_val)
                    visited_count += 1
        
        return visited_count

    def get_distance(self, cube):
        """Returns the real heuristic distance (0-12)"""
        fs_val = cube.get_flip_slice_val()
        ts_val = cube.get_twist_slice_val()
        return max(self.fs_table.get(fs_val), self.ts_table.get(ts_val))