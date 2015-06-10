import cv2
import numpy as np

##number of squares in chessboard
numberOfSquares = 8

##min value for canny-threshold
min_value = 50

turn = 1

##max value for canny-threshold
max_value = 100

## an array having the x and y coordinate of the cornersof the chessboard
corners = [[[0 for a in range(2)] for a in range(numberOfSquares + 1)]for a in range(numberOfSquares + 1)]

##an array having the x and y coordinates of the centres of the chessboard
centres = [[[0 for a in range(2)] for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board after the move is played
piece_presence = [[[0 for a in range(2)] for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board before the move is played
prev_presence  = [[[0 for a in range(2)] for a in range(numberOfSquares)]for a in range(numberOfSquares)]

## determines threshold for checking color of piece
check_color_threshold = 1000

##Dimension of square whose region to be checked for color detection
color_square = 10

##count for edge_detection
edge_there = 555

def photoClick(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
            if not GPIO.input(pin):
                ret, frame = cap.read()
                return ret, frame
            
##function sets the initial conditions at the start of play
def calibrate():
    ##blink false

    while True:
        ret, frame = photoClick(cal)
        if not ret:
            continue
        img = np.copy(frame)
        
        patternsize = ( numberOfSquares + 1, numberOfSquares + 1 )
        corn = cv2.findChessboardCorners( img, patternsize )

        if corn[0]:
            ##calibrating the corners array
            for i in range( 0 , numberOfSquares + 1 ):
                for j in range( 0 , numberOfSquares + 1 ):
                    corners[ i ][ j ][ 0 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 0 ]
                    corners[ i ][ j ][ 1 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 1 ]
                    print corners[i][j]

            ##calibrating the centres array        
            for i in range( 0 , numberOfSquares ):
                for j in range( 0 , numberOfSquares ):
                    centres[ i ][ j ][ 0 ] = (corners[ i ][ j ][ 0 ] + corners[ i+1 ][ j ][ 0 ] + corners[ i ][ j+1 ][ 0 ] + corners[ i+1 ][ j+1 ][ 0 ])/4
                    centres[ i ][ j ][ 1 ] = (corners[ i ][ j ][ 1 ] + corners[ i+1 ][ j ][ 1 ] + corners[ i ][ j+1 ][ 1 ] + corners[ i+1 ][ j+1 ][ 1 ])/4

            ##setting up initial structure of pieces 
            for i in range( 0 , 2 ):
                for j in range( 0 , numberOfSquares ):
                    prev_presence[i][j] = 1
                    prev_presence[numberOfSquares - 1 - i][j] = -1
            ##blink True
            return
    
        
        

##checking whether color of piece is black or white 

## determines threshold for checking color of piece 
threshold1 = 250000
threshold2 = 130000
##checking whether color of piece is black or white 
def check_color( r , c , img ):
    sumyy = 0
    for i in range( int(centres[r][c][0]) - 18 , int(centres[r][c][0]) + 19):
        for j in range( int(centres[r][c][1]) - 18 , int(centres[r][c][1]) + 19):
           sumyy = sumyy + img.item(j,i)
    print r , c, sumyy
    if (r+c)%2==0:
        if sumyy < threshold1:
            return -1
        else:
            return 1
    elif (r+c)%2==1:
        if sumyy > threshold2:
            return 1
        else:
            return -1
##checking whether piece is present or not in a square
def check_presence( image, board  ):
'''
check roi  ke liye side of square
'''
    for row in range( 0 , numberOfSquares ):
        for column in range( 0 , numberOfSquares ):
            roi = image[(corners[row][column][1]+1):(corners[row+1][column+1][1]-1),(corners[row][column][0]+1):(corners[row+1][column+1][0]-1)]
            count = cv2.countNonZero(roi)
            if count > edge_there:
                piece_presence[row][column] = check_color( row , column , board) 
            else:
                piece_presence[row][column] = 0
    return

## comparing board positions before and after move is played and determining the move
def find_move(boardPic):
    board_canny = cv2.Canny ( boardPic , min_value , max_value )
    check_presence( board_canny, boardPic)
    counter = 0
    for i in range( 0 , numberOfSquares ):
        for j in range(0 , numberOfSquares ):
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
            if not previous_presence[numberOfSquares - 1][0] == piece_presence[numberOfSquares - 1][0]:
                b = [ numberOfSquares - 1 , 4 , numberOfSquares - 1 , 2 ]
            else :
                b = [ numberOfSquares - 1 , 4 , numberOfSquares - 1 , 6 ]

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
def update():
    for i in range( 0 , numberOfSquares ):
        for j in range(0 , numberOfSquares):
            previous_presence[i][j] = piece_presence[i][j]
    turn = -turn


#######MAIN CODE

##Start capturing video
"""
cap = cv2.VideoCapture(0)
calibrate()
"""
##while 1: ##End game condition
    #ret , frame = cap.read()
    ##when key pressed
    ##board   = cv2.imread( 'board.jpg', 0 )
    #board = np.copy(frame)
"""
    board_canny = cv2.Canny ( board , min_value , max_value )
    check_presence( board_canny , board )
    find_move(turn)
"""
    ##seek ans from khujau
    #update( ans )
