from math import comb
import re

class EdgePiece:
    def __init__(self, name, orientation):
        self.name = name
        self.orientation = orientation
        # 0->EO correct, 1->EO incorrect


class CornerPiece:
    """
    name: name
    orientation: 0-> CO correct, 1->clockwise, 2->counter colckwise
    """
    def __init__(self, name, orientation):
        self.name = name
        self.orientation = orientation

class Cube:
    """
        corners: ABCD UVWX
        edges: ABCD LJTR UVWX
    """
    def __init__(self, edgepieces, cornerpieces):
        self.edgepieces = edgepieces 
        self.cornerpieces = cornerpieces 
    
    @staticmethod
    def newcube():
        edges = [
            EdgePiece("A", 0), EdgePiece("B", 0), EdgePiece("C", 0), EdgePiece("D", 0),
            EdgePiece("L", 0), EdgePiece("J", 0), EdgePiece("T", 0), EdgePiece("R", 0),
            EdgePiece("U", 0), EdgePiece("V", 0), EdgePiece("W", 0), EdgePiece("X", 0),
        ]

        corners = [
            CornerPiece("A", 0), CornerPiece("B", 0), CornerPiece("C", 0), CornerPiece("D", 0),
            CornerPiece("U", 0), CornerPiece("V", 0), CornerPiece("W", 0), CornerPiece("X", 0),
        ]
        return Cube(edges, corners)
    

    def copy(self):
        new_edges = [EdgePiece(e.name, e.orientation) for e in self.edgepieces]
        new_corners = [CornerPiece(c.name, c.orientation) for c in self.cornerpieces]
        return Cube(new_edges, new_corners)

    def printcube(self):
        print("Edges:")
        for e in self.edgepieces:
            print(f"{e.name}, orientation={e.orientation}")

        print("\nCorners:")
        for c in self.cornerpieces:
            print(f"{c.name}, orientation={c.orientation}")

    def get_flip_number(self):
        flip_number = 0
        for e in self.edgepieces[:11]:
            flip_number = (flip_number<<1) | e.orientation
        return flip_number
    
    def get_twist_number(self):
        slice_number = 0
        for c in self.cornerpieces[:7]:
            slice_number = slice_number * 3 + c.orientation
        return slice_number

    def get_slice_number(self):
        target = {"L", "J", "T", "R"}
        slice_number = 0
        counting_ones = 0
        for i, e in enumerate(self.edgepieces):
            if e.name in target:
                counting_ones += 1
                slice_number += comb(i, counting_ones)
        return slice_number
    
    def get_flip_slice_val(self):
        return self.get_flip_number() + (self.get_slice_number()*(2**11))
    
    def get_twist_slice_val(self):
        return self.get_twist_number() + (self.get_slice_number()*(3**7))
    
    @classmethod
    def from_stringA(cls, edge_str, corner_str):
        """
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
        eo_sum = 0
        for name, ori_str in edge_matches:
            name = name.upper()
            ori = int(ori_str)

            if name not in valid_edge_names:
                raise ValueError(f"Edge '{name}' is duplicate or invalid.")
            valid_edge_names.remove(name)

            if ori not in [0, 1]:
                raise ValueError(f"Edge '{name}' has invalid orientation: {ori}")
            eo_sum += ori
            new_edges.append(EdgePiece(name, ori))

        new_corners = []
        co_sum = 0
        for name, ori_str in corner_matches:
            name = name.upper()
            ori = int(ori_str)

            if name not in valid_corner_names:
                raise ValueError(f"Corner '{name}' is duplicate or invalid.")
            valid_corner_names.remove(name)

            if ori not in [0, 1, 2]:
                raise ValueError(f"Corner '{name}' has invalid orientation: {ori}")
            
            co_sum += ori
            new_corners.append(CornerPiece(name, ori))

        if eo_sum % 2 != 0:
            raise ValueError(f"Illegal Edges: EO sum ({eo_sum}) must be even.")
        if co_sum % 3 != 0:
            raise ValueError(f"Illegal Corners: CO sum ({co_sum}) must be multiple of 3.")

        print("Validation successful: Cube state is mathematically legal.")
        return cls(new_edges, new_corners)
