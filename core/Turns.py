class CubeTurn:

    @staticmethod
    def Turn_layer(pieces, indices, turns, isedge, isUD, isFB):
        i0, i1, i2, i3 = indices

        if turns == 0: #clockwise
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i3], pieces[i0], pieces[i1], pieces[i2]
            if not isUD:
                if isedge and isFB:
                    pieces[i0].orientation = (pieces[i0].orientation+1)%2
                    pieces[i1].orientation = (pieces[i1].orientation+1)%2
                    pieces[i2].orientation = (pieces[i2].orientation+1)%2
                    pieces[i3].orientation = (pieces[i3].orientation+1)%2
                elif not isedge :
                    pieces[i0].orientation = (pieces[i0].orientation+2)%3
                    pieces[i1].orientation = (pieces[i1].orientation+1)%3
                    pieces[i2].orientation = (pieces[i2].orientation+2)%3
                    pieces[i3].orientation = (pieces[i3].orientation+1)%3
                    return

        elif turns == 1: # counter clockwise
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i1], pieces[i2], pieces[i3], pieces[i0]
            if not isUD:
                if isedge and isFB:
                    pieces[i0].orientation = (pieces[i0].orientation+1)%2
                    pieces[i1].orientation = (pieces[i1].orientation+1)%2
                    pieces[i2].orientation = (pieces[i2].orientation+1)%2
                    pieces[i3].orientation = (pieces[i3].orientation+1)%2
                elif not isedge :
                    pieces[i0].orientation = (pieces[i0].orientation+2)%3
                    pieces[i1].orientation = (pieces[i1].orientation+1)%3
                    pieces[i2].orientation = (pieces[i2].orientation+2)%3
                    pieces[i3].orientation = (pieces[i3].orientation+1)%3
                    return

        elif turns == 2: #double
            pieces[i0], pieces[i1], pieces[i2], pieces[i3] = \
            pieces[i2], pieces[i3], pieces[i0], pieces[i1]
            # orientation doesn't change

    @staticmethod
    def U_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [0,1,2,3], turns, True, True, False)
        CubeTurn.Turn_layer(cube.cornerpieces, [0,1,2,3], turns, False, True, False)

    @staticmethod
    def D_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [8,9,10,11], turns, True, True, False)
        CubeTurn.Turn_layer(cube.cornerpieces, [4,5,6,7], turns, False, True, False)

    @staticmethod
    def R_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [1,6,9,5], turns, True, False, False)
        CubeTurn.Turn_layer(cube.cornerpieces, [2,1,6,5], turns, False, False, False)

    @staticmethod
    def L_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [3,4,11,7], turns, True, False, False)
        CubeTurn.Turn_layer(cube.cornerpieces, [0,3,4,7], turns,False,False, False)
    
    @staticmethod
    def F_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [2,5,8,4], turns,True, False,True)
        CubeTurn.Turn_layer(cube.cornerpieces, [3,2,5,4], turns,False, False,True)

    @staticmethod
    def B_Turn(cube, turns):
        CubeTurn.Turn_layer(cube.edgepieces, [0,7,10,6], turns, True,False,True)
        CubeTurn.Turn_layer(cube.cornerpieces, [1,0,7,6], turns,False,False,True)

    

    