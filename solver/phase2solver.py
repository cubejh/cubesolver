class Phase2Solver:
    def __init__(self, table_manager_p2):
        self.tm = table_manager_p2
        self.move_list = self.tm.moves 
        self.num_moves = len(self.move_list)
        
        self.face_map = {'U':0, 'D':1, 'L':2, 'R':3, 'F':4, 'B':5}
        self.opposite_faces = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

    def solve(self, cube, max_depth=18):
        # 取得 Phase 2 的兩個關鍵座標
        start_cp_mp = cube.get_cp_mp_val()
        start_ep_mp = cube.get_ep_mp_val()
        
        # --- 修正處：將 cp_table 改為 cp_mp_table，ep_table 改為 ep_mp_table ---
        initial_h = max(self.tm.cp_mp_table.get(start_cp_mp), 
                        self.tm.ep_mp_table.get(start_ep_mp))
        
        if initial_h == 0:
            # print("Cube is already solved.")
            return ""
        
        for limit in range(initial_h, max_depth + 1):
            self.path = []
            if self._dfs(start_cp_mp, start_ep_mp, 0, limit, -10):
                solution = self._format_path(self.path)
                return solution
        return None

    def _dfs(self, cp_mp, ep_mp, dist, limit, last_face_idx):
        # --- 修正處：這裡也要改名字 ---
        h = max(self.tm.cp_mp_table.get(cp_mp), self.tm.ep_mp_table.get(ep_mp))
        
        if h == 0:
            return True
        if dist + h > limit:
            return False

        for m_idx in range(self.num_moves):
            face, amount = self.move_list[m_idx]
            face_idx = self.face_map[face]

            if face_idx == last_face_idx: continue
            if face_idx == self.opposite_faces.get(last_face_idx):
                if face_idx < last_face_idx: continue
            
            # --- 修正處：確認 Move Table 名字是否正確 ---
            # 根據你 TableManagerP2 的定義，應該是 cp_mp_move 和 ep_mp_move
            next_cp_mp = self.tm.cp_mp_move[cp_mp * self.num_moves + m_idx]
            next_ep_mp = self.tm.ep_mp_move[ep_mp * self.num_moves + m_idx]

            if self._dfs(next_cp_mp, next_ep_mp, dist + 1, limit, face_idx):
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