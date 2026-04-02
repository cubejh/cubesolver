from cube import Cube
from notation import parse_moves

cube  = Cube.newcube()

s1 = "U'"
print("\ntest:")
for m in parse_moves(s1):
    print(m.face, m.amount)
    m.apply(cube)
cube.printcube()


