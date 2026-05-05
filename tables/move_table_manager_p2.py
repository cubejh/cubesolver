import os, time
import multiprocessing as mp
from array import array
from core.cube import Cube
from core.Turns import CubeTurn

def _cp_mp_worker(start, end, num_moves, moves_list):
    local_table = array('i', [-1] * ((end - start) * num_moves))
    for val in range(start, end):
        cube = Cube.from_cp_mp_val(val)
        for m_idx, (face, amount) in enumerate(moves_list):
            child_cube = cube.copy()
            getattr(CubeTurn, f"{face}_Turn")(child_cube, amount)
            child_val = child_cube.get_cp_mp_val()
            local_table[(val - start) * num_moves + m_idx] = child_val
    return local_table

def _ep_mp_worker(start, end, num_moves, moves_list):
    local_table = array('i', [-1] * ((end - start) * num_moves))
    for val in range(start, end):
        cube = Cube.from_ep_mp_val(val)
        for m_idx, (face, amount) in enumerate(moves_list):
            child_cube = cube.copy()
            getattr(CubeTurn, f"{face}_Turn")(child_cube, amount)
            child_val = child_cube.get_ep_mp_val()
            local_table[(val - start) * num_moves + m_idx] = child_val
    return local_table

class MoveTableManagerP2:
    def __init__(self, folder="tables"):
        self.folder = folder
        # 8! * 4! = 967,680
        self.P2_SIZE = 40320 * 24
        self.moves = [
            ('U', 0), ('U', 1), ('U', 2),
            ('D', 0), ('D', 1), ('D', 2),
            ('L', 2), ('R', 2), ('F', 2), ('B', 2)
        ]
        self.num_moves = len(self.moves)

    def build_or_load_move_tables(self):
        cp_path = os.path.join(self.folder, "cp_mp_move.bin")
        ep_path = os.path.join(self.folder, "ep_mp_move.bin")

        if os.path.exists(cp_path) and os.path.exists(ep_path):
            print("Loading Phase 2 move tables...")
            cp_move = array('i'); ep_move = array('i')
            with open(cp_path, 'rb') as f: cp_move.fromfile(f, self.P2_SIZE * self.num_moves)
            with open(ep_path, 'rb') as f: ep_move.fromfile(f, self.P2_SIZE * self.num_moves)
            return cp_move, ep_move
        else:
            print("Phase 2 Move tables not found. Starting Generation...")
            start = time.time()
            cp_move = self._generate_parallel(self.P2_SIZE, _cp_mp_worker)
            self._save(cp_move, cp_path)
            ep_move = self._generate_parallel(self.P2_SIZE, _ep_mp_worker)
            self._save(ep_move, ep_path)
            print(f"Phase 2 Move tables built in {time.time()-start:.2f}s")
            return cp_move, ep_move

    def _generate_parallel(self, total_size, worker_func):
        cpu_count = mp.cpu_count()
        chunk = total_size // cpu_count
        tasks = [(i*chunk, total_size if i==cpu_count-1 else (i+1)*chunk, self.num_moves, self.moves) for i in range(cpu_count)]
        with mp.Pool(cpu_count) as pool:
            res = pool.starmap(worker_func, tasks)
        combined = array('i')
        for r in res: combined.extend(r)
        return combined

    def _save(self, table, path):
        with open(path, 'wb') as f: table.tofile(f)