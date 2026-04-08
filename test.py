from cube import Cube
from Turns import CubeTurn
from notation import parse_moves
from p1_table import TableManager

cube = Cube.newcube()
manager = TableManager()
manager.build_step1_tables()
print(f"(solved cube) moves needed to DR: {manager.get_table_value(cube)}")
CubeTurn.R_Turn(cube, 2)
print(f"(Scramble is an R2) moves needed to DR: {manager.get_table_value(cube)}")
CubeTurn.B_Turn(cube, 1)
print(f"(Scramble is  B') moves needed to DR: {manager.get_table_value(cube)}")
CubeTurn.B_Turn(cube, 0)
CubeTurn.F_Turn(cube, 2)
print(f"(Scramble is  U') moves needed to DR: {manager.get_table_value(cube)}")

"""
manager = TableManager()
manager.build_tables() 
CubeTurn.R_Turn(cube, 1)
val = manager.get_table_value(cube)
print(val)
"""
"""
s1 = "U2 F' L2 R2 D2 B' U2 F2 D2 R2 F L' U R' U2 B D2 R D2 R"
#s1 = "F"
print("\ntest:")
for m in parse_moves(s1):
    print(m.face, m.amount)
    m.apply(cube)
cube.printcube()
print(f"flip_number: {cube.get_flip_number()}")
print(f"twist_number: {cube.get_twist_number()}")
print(f"slice_number: {cube.get_slice_number()}")
print(f"flip_slice_val: {cube.get_flip_slice_val()}")
print(f"twist_slice_val: {cube.get_twist_slice_val()}")
"""

