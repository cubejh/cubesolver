import time
from cube import Cube

class Phase1Solver:
    def __init__(self, table_manager):
        self.tm = table_manager

        self.move_list = self.tm.moves 
        self.num_moves = len(self.move_list)
        
        self.face_map = {'U':0, 'D':1, 'L':2, 'R':3, 'F':4, 'B':5}
        self.opposite_faces = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

    def solve(self, cube, max_depth=20):
        start_fs = cube.get_flip_slice_val()
        start_ts = cube.get_twist_slice_val()
        
        initial_h = max(self.tm.fs_table.get(start_fs), self.tm.ts_table.get(start_ts))
        print(f"Initial Phase 1 Distance: {initial_h}")
        
        if initial_h == 0:
            print("Cube is already in Phase 2 (DR) state.")
            return ""

        print("Searching for Phase 1 solution...")
        start_time = time.time()
        
        for limit in range(initial_h, max_depth + 1):
            self.path = []
            # last_face_idx 設為 -10 避免與 0~5 衝突
            if self._dfs(start_fs, start_ts, 0, limit, -10):
                elapsed = time.time() - start_time
                solution = self._format_path(self.path)
                print(f"Found Solution at depth {limit} ({elapsed:.2f}s): {solution}")
                return solution
            print(f"Depth {limit} finished...", end='\r')
        
        print("No solution found.")
        return None

    def _dfs(self, fs, ts, dist, limit, last_face_idx):
        h = max(self.tm.fs_table.get(fs), self.tm.ts_table.get(ts))
        
        if h == 0:
            return True
        if dist + h > limit:
            return False

        for m_idx in range(self.num_moves):
            face, amount = self.move_list[m_idx]
            face_idx = self.face_map[face]

            if face_idx == last_face_idx:
                continue
            if face_idx == self.opposite_faces.get(last_face_idx):
                if face_idx < last_face_idx:
                    continue
            
            next_fs = self.tm.fs_move[fs * self.num_moves + m_idx]
            next_ts = self.tm.ts_move[ts * self.num_moves + m_idx]

            if self._dfs(next_fs, next_ts, dist + 1, limit, face_idx):
                self.path.append(m_idx)
                return True
        return False

    def _format_path(self, path):
        res = []
        for m_idx in reversed(path):
            face, amount = self.move_list[m_idx]
            suffix = ""
            if amount == 1: suffix = "'"
            elif amount == 2: suffix = "2"
            res.append(f"{face}{suffix}")
        return " ".join(res)

if __name__ == "__main__":
    from p1_table import TableManager
    from notation import parse_moves
    import os

    tm = TableManager(folder="cube_data")
    solver = Phase1Solver(tm)

    cube = Cube.newcube()
    scramble = "R' U' F L2 F' R2 B U2 B R2 B2 D2 R B' F2 D U B D2 L U F R' U' F U2 R U2 R" 
    print(f"Scrambling with: {scramble}")
    for m in parse_moves(scramble):
        m.apply(cube)

    cube2 = Cube.from_stringA("R1B1L0A1X0D1V1C1W0T0U0J0", "X0D0V0A2C2B1W1U0")
    solver.solve(cube)