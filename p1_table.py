from cube import Cube
from twobitarray import BitArray2
from Turns import CubeTurn


class TableManager:
    def __init__(self):
        self.fs_table = BitArray2((2**11)*495)
        self.ts_table = BitArray2((3**7)*495)
        self.ts_table.set(150903,0)
        self.fs_table.set(141312,0)
        self.cube = Cube.newcube()
        self.moves = [(f,a) for f in ['U','D','R','L','F','B'] for a in [0,1,2]]

    def build_step1_tables(self):
        cube = Cube.newcube()
        for face, amount in self.moves:
            cube_copy = cube.copy()
            getattr(CubeTurn, f"{face}_Turn")(cube_copy, amount)
            fs_val = cube_copy.get_flip_slice_val()
            ts_val = cube_copy.get_twist_slice_val()
            if self.fs_table.get(fs_val)==3:
                self.fs_table.set(fs_val, 1)
            if self.ts_table.get(ts_val) ==3:
                self.ts_table.set(ts_val, 1)

    def get_table_value(self, cube):
        fs_val = cube.get_flip_slice_val()
        ts_val = cube.get_twist_slice_val()
        return max(self.fs_table.get(fs_val), self.ts_table.get(ts_val))