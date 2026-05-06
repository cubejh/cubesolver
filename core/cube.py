from math import comb
import math
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
    

    #for phase1 
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
    
    def set_flip(self, val):
        parity = 0
        for i in range(10, -1, -1):
            ori = (val >> (10 - i)) & 1
            self.edgepieces[i].orientation = ori
            parity += ori
        self.edgepieces[11].orientation = parity % 2

    def set_twist(self, val):
        lastc = 0
        for i in range(6, -1, -1):
            ori = val % 3
            val //= 3
            self.cornerpieces[i].orientation = ori
            lastc += ori
        self.cornerpieces[7].orientation = (3 - (lastc % 3)) % 3

    def set_slice(self, val):
        for e in self.edgepieces:
            e.name = ""
        k = 4
        for i in range(11, -1, -1):
            if val >= comb(i, k):
                val -= comb(i, k)
                self.edgepieces[i].name = ["L", "J", "T", "R"][k-1]
                k -= 1
            if k == 0: break
        others = ["A", "B", "C", "D", "U", "V", "W", "X"]
        idx = 0
        for e in self.edgepieces:
            if e.name == "":
                e.name = others[idx]
                idx += 1

    @staticmethod
    def from_fs_val(val):
        c = Cube.newcube()
        c.set_flip(val % 2048)
        c.set_slice(val // 2048)
        return c

    @staticmethod
    def from_ts_val(val):
        c = Cube.newcube()
        c.set_twist(val % 2187)
        c.set_slice(val // 2187)
        return c

    # for phase 2
    @staticmethod
    def get_rank(perm):
        rank = 0
        for i in range(len(perm)):
            count = 0
            for j in range(i + 1, len(perm)):
                if perm[j] < perm[i]: count += 1
            rank += count * math.factorial(len(perm) - 1 - i)
        return rank

    @staticmethod
    def set_rank(rank, n):
        items = list(range(n))
        res = []
        for i in range(n - 1, -1, -1):
            f = math.factorial(i)
            idx = rank // f
            rank %= f
            res.append(items.pop(idx))
        return res
    
    def get_cp_val(self):
        names = [c.name for c in self.cornerpieces]
        mapping = {"A":0,"B":1,"C":2,"D":3,"U":4,"V":5,"W":6,"X":7}
        perm = [mapping[n] for n in names]
        return self.get_rank(perm)

    def get_ep_val(self):

        target = ["A","B","C","D","U","V","W","X"]
        perm = []
        for e in self.edgepieces:
            if e.name in target:
                perm.append(target.index(e.name))
        return self.get_rank(perm)

    def get_mp_val(self):
        target = ["L","J","T","R"]
        perm = []
        for e in self.edgepieces:
            if e.name in target:
                perm.append(target.index(e.name))
        return self.get_rank(perm)

    def get_cp_mp_val(self):
        return self.get_cp_val() * 24 + self.get_mp_val()

    def get_ep_mp_val(self):
        return self.get_ep_val() * 24 + self.get_mp_val()
    
    def set_cp_mp(self, val):
        cp_rank = val // 24
        mp_rank = val % 24
        
        cp_perm = self.set_rank(cp_rank, 8)
        names = ["A","B","C","D","U","V","W","X"]
        for i in range(8):
            self.cornerpieces[i].name = names[cp_perm[i]]
            self.cornerpieces[i].orientation = 0 # Phase 2 預設方向已好

        mp_perm = self.set_rank(mp_rank, 4)
        mp_names = ["L","J","T","R"]
        for e in self.edgepieces: e.name = ""
        for i, pos in enumerate([4, 5, 6, 7]): 
            self.edgepieces[pos].name = mp_names[mp_perm[i]]
            self.edgepieces[pos].orientation = 0

    def set_ep_mp(self, val):
        ep_rank = val // 24
        mp_rank = val % 24
        
        ep_perm = self.set_rank(ep_rank, 8)
        ep_names = ["A","B","C","D","U","V","W","X"]

        mp_perm = self.set_rank(mp_rank, 4)
        mp_names = ["L","J","T","R"]

        ud_indices = [0,1,2,3,8,9,10,11]
        for i, pos in enumerate(ud_indices):
            self.edgepieces[pos].name = ep_names[ep_perm[i]]
        
        for i, pos in enumerate([4,5,6,7]):
            self.edgepieces[pos].name = mp_names[mp_perm[i]]

    @staticmethod
    def from_cp_mp_val(val):
        c = Cube.newcube()
        c.set_cp_mp(val)
        return c

    @staticmethod
    def from_ep_mp_val(val):
        c = Cube.newcube()
        c.set_ep_mp(val)
        return c

