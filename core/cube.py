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