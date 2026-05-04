import os
from collections import deque
from array import array
import time
from core.cube import Cube
from core.Turns import CubeTurn
from tables.distance_table import DistanceTable

class MoveTableManager:
    def __init__(self, folder="tables"):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.FS_SIZE = (2**11) * 495
        self.TS_SIZE = (3**7) * 495
        self.moves = [(f, a) for f in ['U', 'D', 'R', 'L', 'F', 'B'] for a in [0, 1, 2]]
        self.num_moves = len(self.moves)

    def build_or_load_move_tables(self):
        fs_path = os.path.join(self.folder, "fs_move.bin")
        ts_path = os.path.join(self.folder, "ts_move.bin")

        if os.path.exists(fs_path) and os.path.exists(ts_path):
            print("Loading move tables from disk...")
            fs_move = array('i')
            with open(fs_path, 'rb') as f:
                fs_move.fromfile(f, self.FS_SIZE * self.num_moves)
            ts_move = array('i')
            with open(ts_path, 'rb') as f:
                ts_move.fromfile(f, self.TS_SIZE * self.num_moves)
            return fs_move, ts_move
        else:
            print("Move tables not found. Starting generation (this may take a few minutes)...")
            
            build_start = time.time()
            
            fs_move = self._build_move_table(self.FS_SIZE, "get_flip_slice_val")
            self._save_move_table(fs_move, fs_path)
            
            ts_move = self._build_move_table(self.TS_SIZE, "get_twist_slice_val")
            self._save_move_table(ts_move, ts_path)

            build_end = time.time()
            print(f"move tables built and saved in {build_end - build_start:.2f} seconds.")
            
            return fs_move, ts_move

    def _build_move_table(self, size, val_func_name):
        move_table = array('i', [-1] * (size * self.num_moves))
        start_cube = Cube.newcube()
        start_val = getattr(start_cube, val_func_name)()
        
        queue = deque([start_cube])
        visited = DistanceTable(size)
        visited.set(start_val, 1)

        count = 1
        while queue:
            curr_cube = queue.popleft()
            curr_val = getattr(curr_cube, val_func_name)()

            for move_idx, (face, amount) in enumerate(self.moves):
                child_cube = curr_cube.copy()
                getattr(CubeTurn, f"{face}_Turn")(child_cube, amount)
                child_val = getattr(child_cube, val_func_name)()
                
                move_table[curr_val * self.num_moves + move_idx] = child_val
                
                if visited.get(child_val) == 255: # 255 means unvisited
                    visited.set(child_val, 1)
                    queue.append(child_cube)
                    count += 1
                    if count % 50000 == 0:
                        print(f"Progress: {count}/{size} states explored...", end='\r')
        
        print(f"\nMove table built. Total unique states found: {count}")
        return move_table

    def _save_move_table(self, move_table, path):
        with open(path, 'wb') as f:
            move_table.tofile(f)