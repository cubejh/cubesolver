from dataclasses import dataclass
from core.Turns import CubeTurn
import re

@dataclass
class Move:
    face: str
    amount: int

    def apply(self, cube):
        move_map = {
            'U': CubeTurn.U_Turn,
            'D': CubeTurn.D_Turn,
            'R': CubeTurn.R_Turn,
            'L': CubeTurn.L_Turn,
            'F': CubeTurn.F_Turn,
            'B': CubeTurn.B_Turn,
        }
        move_map[self.face](cube, self.amount)

def parse_moves(s: str) -> list[Move]:
    s = s.replace(" ","")
    moves = []
    
    tokens = re.findall(r"[A-Z][^A-Z]*", s) 
    for t in tokens:
        face = t[0]
        
        if len(t) == 1:
            amount = 0
        elif t[1] == "'":
            amount = 1
        elif t[1] == "2":
            amount = 2
        else:
            raise ValueError(f"Invalid move: {t}")
        
        moves.append(Move(face, amount))
    
    return moves

"""
example:
s1 = "R' L B' D2 L2 B2 L' D R' L2 F2 B2 D R2 U' D' L2 F2 D' R2"
print("\ntest:")
for m in parse_moves(s1):
    print(m.face, m.amount)
    m.apply(cube)
"""