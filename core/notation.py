from dataclasses import dataclass
from core.Turns import CubeTurn
from core.cube import CornerPiece, EdgePiece, Cube
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

def parity_analysis(paritylist):
    parity = 0
    for i in range(0,len(paritylist)-1):
        for j in range(0,len(paritylist)-1-i):
            if ord(paritylist[j]) > ord(paritylist[j+1]) :
                paritylist[j],paritylist[j+1] = paritylist[j+1], paritylist[j]
                parity = parity + 1
    return parity%2

def from_piece_orient_init(edge_str, corner_str):
    """
    piecesname + orientation
    edge example: B0C1A1D1L1J1T0R1U0V1W1X0
    corner example: B0A1C0D2V0U0W1X2
    """
    
    def extract_tokens(s):
        return re.findall(r"([A-Za-z])(\d+)", s)

    edge_matches = extract_tokens(edge_str)
    corner_matches = extract_tokens(corner_str)

    if len(edge_matches) != 12:
        raise ValueError(f"Edges error: expected 12, found {len(edge_matches)} in '{edge_str}'")
    if len(corner_matches) != 8:
        raise ValueError(f"Corners error: expected 8, found {len(corner_matches)} in '{corner_str}'")

    valid_edge_names = set("ABCDLJTRUVWX")
    valid_corner_names = set("ABCDUVWX")

    new_edges = []
    edge_parity = []
    eo_sum = 0
    for name, ori_str in edge_matches:
        name = name.upper()
        ori = int(ori_str)

        if name not in valid_edge_names:
            raise ValueError(f"Edge '{name}' is duplicate or invalid.")
        valid_edge_names.remove(name)
        edge_parity += name

        if ori not in [0, 1]:
            raise ValueError(f"Edge '{name}' has invalid orientation: {ori}")
        eo_sum += ori
        new_edges.append(EdgePiece(name, ori))

    new_corners = []
    corner_parity = []
    co_sum = 0
    for name, ori_str in corner_matches:
        name = name.upper()
        ori = int(ori_str)

        if name not in valid_corner_names:
            raise ValueError(f"Corner '{name}' is duplicate or invalid.")
        valid_corner_names.remove(name)
        corner_parity += name

        if ori not in [0, 1, 2]:
            raise ValueError(f"Corner '{name}' has invalid orientation: {ori}")
        
        co_sum += ori
        new_corners.append(CornerPiece(name, ori))

    if eo_sum % 2 != 0:
        raise ValueError(f"Illegal Edges: EO sum ({eo_sum}) must be even.")
    if co_sum % 3 != 0:
        raise ValueError(f"Illegal Corners: CO sum ({co_sum}) must be multiple of 3.")
    if (parity_analysis(edge_parity)+parity_analysis(corner_parity)) ==1:
         raise ValueError(f"Illegal State: Parity Test failed.")
    print("Validation successful: Cube state is mathematically legal.")
    return Cube(new_edges, new_corners)

def from_piece_def_init(edge_str, corner_str):
        
    def extract_tokens(s):
        return re.findall(r"[A-Za-z]", s)

    edge_matches = extract_tokens(edge_str)
    corner_matches = extract_tokens(corner_str)

    if len(edge_matches) != 12:
        raise ValueError(f"Edges error: expected 12, found {len(edge_matches)} in '{edge_str}'")
    if len(corner_matches) != 8:
        raise ValueError(f"Corners error: expected 8, found {len(corner_matches)} in '{corner_str}'")

    valid_edge_names = set("ABCDEFGHIJKLMNOPQRSTUVWX")
    edge_pair_map = {
                    "A": ("Q",0,"A"), "Q": ("A",1,"A"),
                    "B": ("M",0,"B"), "M": ("B",1,"B"),
                    "C": ("I",0,"C"), "I": ("C",1,"C"),
                    "D": ("E",0,"D"), "E": ("D",1,"D"),
                    "F": ("L",1,"L"), "L": ("F",0,"L"),
                    "G": ("X",1,"X"), "X": ("G",0,"X"),
                    "H": ("R",1,"R"), "R": ("H",0,"R"),
                    "J": ("P",0,"J"), "P": ("J",1,"J"),
                    "K": ("U",1,"U"), "U": ("K",0,"U"),
                    "N": ("T",1,"T"), "T": ("N",0,"T"),
                    "O": ("V",1,"V"), "V": ("O",0,"V"),
                    "S": ("W",1,"W"), "W": ("S",0,"W"),
    }
    valid_corner_names = set("ABCDEFGHIJKLMNOPQRSTUVWX")
    corner_pair_map = {
                        "A": ("E","R",0,"A"), "E": ("A","R",2,"A"), "R": ("A","E",1,"A"),
                        "B": ("Q","N",0,"B"), "Q": ("B","N",2,"B"), "N": ("Q","B",1,"B"),
                        "C": ("M","J",0,"C"), "M": ("C","J",2,"C"), "J": ("C","M",1,"C"),
                        "D": ("I","F",0,"D"), "I": ("D","F",2,"D"), "F": ("D","I",1,"D"),
                        "U": ("G","L",0,"U"), "G": ("U","L",2,"U"), "L": ("U","G",1,"U"),
                        "V": ("K","P",0,"V"), "K": ("V","P",2,"V"), "P": ("K","V",1,"V"),
                        "W": ("O","T",0,"W"), "O": ("W","T",2,"W"), "T": ("O","W",1,"W"),
                        "X": ("S","H",0,"X"), "S": ("X","H",2,"X"), "H": ("X","S",1,"X"),
    }

    new_edges = []
    edge_parity = []
    eo_sum = 0
    for edgecode in edge_matches:
        name = edgecode.upper()
        if name not in valid_edge_names:
            raise ValueError(f"Edge '{name}' is duplicate or invalid.")
        
        if name in edge_pair_map:
            other, ori, record_name = edge_pair_map[name]
            valid_edge_names -= {name, other}
            edge_parity += record_name
            eo_sum += ori
            new_edges.append(EdgePiece(record_name, ori))

    new_corners = []
    corner_parity = []
    co_sum = 0
    for corner_code in corner_matches:
        name = corner_code.upper()
        if name not in valid_corner_names:
            raise ValueError(f"Corner '{name}' is duplicate or invalid.")

        if name in corner_pair_map:
            other1, other2, ori, record_name = corner_pair_map[name]
            valid_corner_names -= {name, other1, other2}
            corner_parity += record_name
            co_sum += ori
            new_corners.append(CornerPiece(record_name, ori))

    if eo_sum % 2 != 0:
        raise ValueError(f"Illegal Edges: EO sum ({eo_sum}) must be even.")
    if co_sum % 3 != 0:
        raise ValueError(f"Illegal Corners: CO sum ({co_sum}) must be multiple of 3.")
    if (parity_analysis(edge_parity)+parity_analysis(corner_parity)) ==1:
         raise ValueError(f"Illegal State: Parity Test failed.")
    print("Validation successful: Cube state is mathematically legal.")
    return Cube(new_edges, new_corners)

