import cv2
import numpy as np

## an array having the x and y coordinate of the cornersof the chessboard
corners = [[[0 for a in range(2)] for a in range(9)]for a in range(9)]

##an array having the x and y coordinates of the centres of the chessboard
centres = [[[0 for a in range(2)] for a in range(8)]for a in range(8)]

##an array storing the structure of the board after the move is played
piece_presence = [[[0 for a in range(2)] for a in range(8)]for a in range(8)]

##an array storing the structure of the board before the move is played
prev_presence  = [[[0 for a in range(2)] for a in range(8)]for a in range(8)]

##determines whos turn it is
turn = 1

## determines threshold for checking color of piece 
threshold = 30000

##function sets the initial conditions at the start of play
def calibrate():

    ####click photo left ##check when pressed
    img = np.copy(frame)
##    img = cv2.imread( 'emptyboard.jpg', 1 )
    patternsize = ( 9,9 )
    corn = cv2.findChessboardCorners( img, patternsize )

    ##calibrating the corners array
    for i in range( 0 , 9 ):
        for j in range( 0 , 9 ):
            corners[ i ][ j ][ 0 ] = corn[ 1 ][ 9*i+j, 0, 0 ]
            corners[ i ][ j ][ 1 ] = corn[ 1 ][ 9*i+j, 0, 1 ]
            print corners[i][j]

    ##calibrating the centres array        
    for i in range( 0 , 8 ):
        for j in range( 0 , 8 ):
            centres[ i ][ j ][ 0 ] = (corners[ i ][ j ][ 0 ] + corners[ i+1 ][ j ][ 0 ] + corners[ i ][ j+1 ][ 0 ] + corners[ i+1 ][ j+1 ][ 0 ])/4
            centres[ i ][ j ][ 1 ] = (corners[ i ][ j ][ 1 ] + corners[ i+1 ][ j ][ 1 ] + corners[ i ][ j+1 ][ 1 ] + corners[ i+1 ][ j+1 ][ 1 ])/4

    ##setting up initial structure of pieces 
    for i in range( 0 , 2 ):
        for j in range( 0 , 8 ):
            prev_presence[i][j] = 1
            prev_presence[7-i][j] = -1
    return

##checking whether color of piece is black or white 
def check_color( r , c , img ):
    sumyy = 0
    for i in range( centres[r][c][0] - 20 , centres[r][c][0] + 20):
        for j in range( centres[r][c][1] - 20 , centres[r][c][1] + 20):
           sumyy = sumyy + img.item(i,j)
    if sumyy < threshold:
        return -1
    else:
        return 1

##checking whether piece is present or not in a square
def check_presence( image, board  ):
    for row in range( 0 , 8 ):
        for column in range( 0 , 8 ):
            roi = image[(corners[row][column][1]+1):(corners[row+1][column+1][1]-1),(corners[row][column][0]+1):(corners[row+1][column+1][0]-1)]
            count = cv2.countNonZero(roi)
            if count > 700:
                piece_presence[row][column] = check_color( row , column , board) 
            else:
                piece_presence[row][column] = 0
    return

## comparing board positions before and after move is played and determining the move
def find_move ():
    counter = 0
    for i in range( 0 , 8 ):
        for j in range(0 , 8):
            if not previous_presence[i][j] == piece_presence[i][j]:
                counter++
                if piece_presence[i][j] == turn : 
                    fr = i
                    fc = j
                else :
                    ir = i
                    ic = j

    ## normal move or capture
    if counter == 2 :
        b = [ir , ic , fr , fc ]

    ## castling
    elif counter == 4 :
        if turn == 1 : ##whites turn
            if not previous_presence[0][0] == piece_presence[0][0]:
                b = [ 0 , 4 , 0 , 2 ]
            else :
                b = [ 0 , 4 , 0 , 6 ]
                
        else : ## blacks turn
            if not previous_presence[7][0] == piece_presence[7][0]:
                b = [ 7 , 4 , 7 , 2 ]
            else :
                b = [ 7 , 4 , 7 , 6 ]

    ## en - passent
    else :
        if turn == 1:
            if not previous_presence[fr - 1][fc - 1] == piece_presence[fr - 1][fc - 1]:
                ir = fr - 1
                ic = fc - 1
                
            else:
                ir = fr - 1
                ic = fc + 1
                
        else :
            if not previous_presence[fr + 1][fc - 1] == piece_presence[fr + 1][fc - 1]:
                ir = fr + 1
                ic = fc - 1
                
            else:
                ir = fr + 1
                ic = fc + 1

        b = [ ir , ic ,fr , fc]
        
        return b
    

## updates after determining whether mov is legal or not
def update ( ans ):
    if ans == True:
        for i in range( 0 , 8 ):
            for j in range(0 , 8):
                previous_presence[i][j] = piece_presence[i][j]
        turn = -turn


#######MAIN CODE

##Start capturing video
cap = cv2.VideoCapture(0)
calibrate()
while 1: ##End game condition
    ret , frame = cap.read()
    ##when key pressed
    ##board   = cv2.imread( 'board.jpg', 0 )
    board = np.copy(frame)
    board_canny = cv2.Canny ( board , 11 , 90 )
    check_presence( board_canny , board )
    find_move(turn)

    ##seek ans from khujau
    update( ans )
