import os
import time
from core.cube import Cube
from core.notation import parse_moves, from_piece_def_init, from_piece_orient_init
from tables.p1_table import TableManager
from tables.p2_table import TableManagerP2
from solver.phase1solver import Phase1Solver
from solver.phase2solver import Phase2Solver

class CubeSolver:
    def __init__(self, data_folder="cube_data"):
        print("--- Initializing Cube Solver (Loading Tables) ---")
        start_time = time.time()
        
        self.tm1 = TableManager(folder=data_folder)
        self.tm2 = TableManagerP2(folder=data_folder)
        
        self.solver1 = Phase1Solver(self.tm1)
        self.solver2 = Phase2Solver(self.tm2)
        
        print(f"Solver ready. Tables loaded in {time.time() - start_time:.2f}s\n")

    def solve(self, cube):
        
        # Phase 1
        solution1 = self.solver1.solve(cube)
        if not solution1 and solution1 != "": 
             print("Failed to find Phase 1 solution.")
             return None
        
        p1_moves = parse_moves(solution1)
        for m in p1_moves:
            m.apply(cube)
            
        # Phase 2
        solution2 = self.solver2.solve(cube)
        if solution2 is None:
            print("Failed to find Phase 2 solution.")
            return None

        full_solution = f"{solution1} {solution2}".strip()
        full_solution = self.simplify_moves(full_solution)
        
        
        print(f"Full Solution: {full_solution}")
        print(f"Steps: {len(full_solution.split())}")
        
        return full_solution

    def solve_scramble(self, scramble):
        """"""
        print(f"Scramble: {scramble}")
        cube = Cube.newcube()
        for m in parse_moves(scramble):
            m.apply(cube)
        return self.solve(cube)

    def solve_piece_def(self, edge_string, corner_string):
        """"""
        cube = from_piece_def_init(edge_string, corner_string)
        return self.solve(cube)
    
    def solve_piece_orientation_def(self, edge_string, corner_string):
        """"""
        cube = from_piece_orient_init(edge_string, corner_string)
        return self.solve(cube)

    @staticmethod
    def simplify_moves(move_str):
        """"""
        if not move_str: return ""
        moves = move_str.split()
        simplified = []
        for move in moves:
            face = move[0]
            amount = 1
            if len(move) > 1:
                if move[1] == '2': amount = 2
                elif move[1] == "'": amount = 3
            
            if simplified and simplified[-1][0] == face:
                prev_face, prev_amount = simplified.pop()
                new_amount = (prev_amount + amount) % 4
                if new_amount != 0:
                    simplified.append((prev_face, new_amount))
            else:
                simplified.append((face, amount))
        
        res = []
        for f, a in simplified:
            if a == 1: res.append(f)
            elif a == 2: res.append(f + "2")
            elif a == 3: res.append(f + "'")
        return " ".join(res)