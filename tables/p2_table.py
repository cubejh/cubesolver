import os
from collections import deque
import time
from core.cube import Cube
from tables.move_table_manager_p2 import MoveTableManagerP2 
from tables.distance_table import DistanceTable

class TableManagerP2:
    def __init__(self, folder="tables"):
        self.folder = folder
        # 8! * 4! = 40320 * 24 = 967,680
        self.P2_SIZE = 40320 * 24
        
        self.moves = [
            ('U', 0), ('U', 1), ('U', 2),
            ('D', 0), ('D', 1), ('D', 2),
            ('L', 2), ('R', 2), ('F', 2), ('B', 2)
        ]
        self.num_moves = len(self.moves)

        # 1. Initialize/Load Phase 2 Move Tables
        move_mgr = MoveTableManagerP2(folder)
        self.cp_mp_move, self.ep_mp_move = move_mgr.build_or_load_move_tables()

        # 2. Initialize Pruning Tables
        self.cp_mp_table = DistanceTable(self.P2_SIZE)
        self.ep_mp_table = DistanceTable(self.P2_SIZE)
        self.load_or_build_pruning()

    def load_or_build_pruning(self):
        cp_path = os.path.join(self.folder, "cp_mp_pruning.bin")
        ep_path = os.path.join(self.folder, "ep_mp_pruning.bin")

        if os.path.exists(cp_path) and os.path.exists(ep_path):
            print("--- Loading Phase 2 pruning tables from disk ---")
            self.cp_mp_table = DistanceTable.from_file(cp_path)
            self.ep_mp_table = DistanceTable.from_file(ep_path)
            print("Phase 2 Pruning tables loaded successfully.")
        else:
            print("--- Starting Phase 2 Pruning Table Generation ---")
            total_start = time.time()
            
            start_cube = Cube.newcube()
            start_cp_mp = start_cube.get_cp_mp_val()
            start_ep_mp = start_cube.get_ep_mp_val()

            # 1. Corner Permutation + MP
            print(f"\nBuilding CP-MP Pruning Table (Size: {self.P2_SIZE})...")
            cp_start = time.time()
            self._build_pruning_table(self.cp_mp_table, self.cp_mp_move, start_cp_mp)
            self.cp_mp_table.to_file(cp_path)
            cp_end = time.time()
            print(f"Finished.")
            print(f"  - Time taken: {cp_end - cp_start:.2f} seconds")
            
            # 2. Edge Permutation + MP
            print(f"\nBuilding EP-MP Pruning Table (Size: {self.P2_SIZE})...")
            ep_start = time.time()
            self._build_pruning_table(self.ep_mp_table, self.ep_mp_move, start_ep_mp)
            self.ep_mp_table.to_file(ep_path)
            ep_end = time.time()
            print(f"Finished.")
            print(f"  - Time taken: {ep_end - ep_start:.2f} seconds")

            total_end = time.time()
            print(f"\n{'='*50}")
            print(f"Phase 2 Pruning tables built and saved in {total_end - total_start:.2f} seconds.")
            print(f"{'='*50}")

    def _build_pruning_table(self, pruning_table, move_table, start_val):
        """BFS"""
        pruning_table.set(start_val, 0)
        queue = deque([start_val])
        visited_count = 1
        
        while queue:
            curr_val = queue.popleft()
            curr_dist = pruning_table.get(curr_val)
            next_dist = curr_dist + 1

            base_idx = curr_val * self.num_moves
            for move_idx in range(self.num_moves):
                child_val = move_table[base_idx + move_idx]
                
                if child_val != -1 and pruning_table.get(child_val) == 255:
                    pruning_table.set(child_val, next_dist)
                    queue.append(child_val)
                    visited_count += 1
        
        return visited_count

    def get_distance(self, cube):
        """
        """
        cp_mp_val = cube.get_cp_mp_val()
        ep_mp_val = cube.get_ep_mp_val()
        return max(self.cp_mp_table.get(cp_mp_val), self.ep_mp_table.get(ep_mp_val))