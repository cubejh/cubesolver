import os
import time
import multiprocessing as mp
from array import array
from core.cube import Cube
from core.Turns import CubeTurn


def _fs_worker(start, end, num_moves, moves_list):
    local_table = array('i', [-1] * ((end - start) * num_moves))
    for val in range(start, end):
        cube = Cube.from_fs_val(val)
        for m_idx, (face, amount) in enumerate(moves_list):
            child_cube = cube.copy()
            getattr(CubeTurn, f"{face}_Turn")(child_cube, amount)
            child_val = child_cube.get_flip_slice_val()
            local_table[(val - start) * num_moves + m_idx] = child_val
    return local_table

def _ts_worker(start, end, num_moves, moves_list):
    local_table = array('i', [-1] * ((end - start) * num_moves))
    for val in range(start, end):
        cube = Cube.from_ts_val(val)
        for m_idx, (face, amount) in enumerate(moves_list):
            child_cube = cube.copy()
            getattr(CubeTurn, f"{face}_Turn")(child_cube, amount)
            child_val = child_cube.get_twist_slice_val()
            local_table[(val - start) * num_moves + m_idx] = child_val
    return local_table

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
            print("\n--- Loading move tables from disk ---")
            fs_move = array('i')
            with open(fs_path, 'rb') as f:
                fs_move.fromfile(f, self.FS_SIZE * self.num_moves)
            ts_move = array('i')
            with open(ts_path, 'rb') as f:
                ts_move.fromfile(f, self.TS_SIZE * self.num_moves)
            print("Tables loaded successfully.")
            return fs_move, ts_move
        else:
            print("\n--- Starting Move Table Generation---")
            total_start = time.time()

            # 1. Flip-Slice Table
            print(f"\nBuilding Flip-Slice Table (Size: {self.FS_SIZE})...")
            fs_start = time.time()
            fs_move = self._generate_parallel(self.FS_SIZE, _fs_worker)
            fs_end = time.time()
            self._print_stats("Flip-Slice Table", fs_start, fs_end)
            self._save_move_table(fs_move, fs_path)

            # 2. Twist-Slice Table
            print(f"\nBuilding Twist-Slice Table (Size: {self.TS_SIZE})...")
            ts_start = time.time()
            ts_move = self._generate_parallel(self.TS_SIZE, _ts_worker)
            ts_end = time.time()
            self._print_stats("Twist-Slice Table", ts_start, ts_end)
            self._save_move_table(ts_move, ts_path)

            total_end = time.time()
            print(f"\n{'='*50}")
            print(f"All tables completed in {total_end - total_start:.2f} seconds.")
            print(f"{'='*50}")
            
            return fs_move, ts_move

    def _generate_parallel(self, total_size, worker_func):
        cpu_count = mp.cpu_count()
        chunk_size = total_size // cpu_count
        tasks = []

        for i in range(cpu_count):
            start = i * chunk_size
            end = total_size if i == cpu_count - 1 else (i + 1) * chunk_size
            tasks.append((start, end, self.num_moves, self.moves))

        # 使用 mp.Pool 進行平行處理
        with mp.Pool(processes=cpu_count) as pool:
            results = pool.starmap(worker_func, tasks)

        combined = array('i')
        for res in results:
            combined.extend(res)
        return combined

    def _print_stats(self, name, start_time, end_time):
        duration = end_time - start_time
        print(f"Finished {name}:")
        print(f"  - Time taken: {duration:.2f} seconds")

    def _save_move_table(self, move_table, path):
        with open(path, 'wb') as f:
            move_table.tofile(f)