class CubeTurn:

    @staticmethod
    def Turn_layer(pieces, indices, turns):
        i0, i1, i2, i3 = indices

        if turns == 0:
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i3], pieces[i0], pieces[i1], pieces[i2]

        elif turns == 1:
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i1], pieces[i2], pieces[i3], pieces[i0]

        elif turns == 2:
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i2], pieces[i3], pieces[i0], pieces[i1]

    @staticmethod
    def U_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [0,1,2,3], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [0,1,2,3], turns)

    @staticmethod
    def D_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [8,9,10,11], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [4,5,6,7], turns)

    @staticmethod
    def R_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [1,5,6,9], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [2,1,6,5], turns)

    @staticmethod
    def L_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [3,4,7,11], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [0,3,4,7], turns)
    
    @staticmethod
    def F_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [2,5,8,4], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [3,2,5,4], turns)

    @staticmethod
    def B_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [0,7,10,6], turns)
        CubeTurn.Turn_layer(cube.cornerpieces, [1,0,7,6], turns)

    

    