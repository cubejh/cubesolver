class EdgePiece:
    def __init__(self, name, orientation):
        self.name = name
        self.orientation = orientation


class CornerPiece:
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
    
    def printcube(self):
        print("Edges:")
        for e in self.edgepieces:
            print(f"{e.name}, orientation={e.orientation}")

        print("\nCorners:")
        for c in self.cornerpieces:
            print(f"{c.name}, orientation={c.orientation}")