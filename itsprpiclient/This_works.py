import cv2
import numpy as np
from math import *

##number of squares in chessboard
numberOfSquares = 8

##determines whose turn it is
turn = 1

##min value for canny-threshold
min_value = 50

##max value for canny-threshold
max_value = 100

## an array having the x and y coordinate of the cornersof the chessboard
corners = [[[0 for a in range(2)] for a in range(numberOfSquares + 1)]for a in range(numberOfSquares + 1)]

##an array having the x and y coordinates of the centres of the chessboard
centres = [[[0 for a in range(2)] for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board after the move is played
piece_presence = [[0 for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board before the move is played
prev_presence  = [[0 for a in range(numberOfSquares)]for a in range(numberOfSquares)]

## determines threshold for checking color of piece
check_color_threshold = 1000

##Dimension of square whose region to be checked for color detection
color_square = 10.0

##count for edge_detection
edge_there = 100

##side of square
square_side = 0

##ratio of side of square to piece
factor = 2
factor_for_t1 = 0.8
factor_for_t2 = 1.2

## determines threshold for checking color of piece 
threshold1 = 0
threshold2 = 0

def threshold_black_in_white(centres , img , s):
    sum_min = 255*s*s
    for row in range( 0 , 8 ):
        for column in range( 0 , 8 ):
            if ((row+column) % 2) == 0:
                sumb = 0
                for j in range(int(s)):
                    for i in range(int(s)):
                        sumb = sumb + img.item(int(centres[row][column][1] - s/2 + i) , int(centres[row][column][0] - s/2 + j))  
                if sumb < sum_min :
                    sum_min = sumb
    return sum_min        

def threshold_white_in_black(centres , img , s):
    sum_max = 0
    for row in range( 0 , 8 ):
        for column in range( 0 , 8 ):
            if ((row+column) % 2) == 1:
                sumb = 0
                for j in range(int(s)):
                    for i in range( int(s)):
                        sumb = sumb + img.item(int(centres[row][column][1] - s/2 + i) , int(centres[row][column][0] - s/2 + j))  
                if sumb > sum_max :
                    sum_max = sumb
    return sum_max     

##def photoClick(pin):
##    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##    while True:
##            if not GPIO.input(pin):
##                ret, frame = cap.read()
##                return ret, frame
##            
##function sets the initial conditions at the start of play
def calibrate(img):
    ##blink false

    patternsize = ( numberOfSquares + 1, numberOfSquares + 1 )
    corn = cv2.findChessboardCorners( img, patternsize )
    cv2.drawChessboardCorners( img, (9,9), corn[1], corn[0])
    cv2.imwrite( 'board.jpg', img)
    print corn[0]
    print corn[1]

    if corn[0]:
        ##calibrating the corners array
        for i in range( 0 , numberOfSquares + 1 ):
            for j in range( 0 , numberOfSquares + 1 ):
                corners[ i ][ j ][ 0 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 0 ]
                corners[ i ][ j ][ 1 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 1 ]
                print corners[i][j]

        x_difference = corners[4][4][0] - corners[4][5][0] 
        y_difference = corners[4][4][1] - corners[4][5][1]
        square_side = sqrt( x_difference*x_difference + y_difference*y_difference)
        
        ##calibrating the centres array        
        for i in range( 0 , numberOfSquares ):
            for j in range( 0 , numberOfSquares ):
                centres[ i ][ j ][ 0 ] = (corners[ i ][ j ][ 0 ] + corners[ i+1 ][ j ][ 0 ] + corners[ i ][ j+1 ][ 0 ] + corners[ i+1 ][ j+1 ][ 0 ])/4
                centres[ i ][ j ][ 1 ] = (corners[ i ][ j ][ 1 ] + corners[ i+1 ][ j ][ 1 ] + corners[ i ][ j+1 ][ 1 ] + corners[ i+1 ][ j+1 ][ 1 ])/4
                
        color_square = 30
        
        threshold1 = threshold_black_in_white(centres , img , color_square)
        threshold2 = threshold_white_in_black(centres , img , color_square)

##        ##setting up initial structure of pieces 
##        for i in range( 0 , 2 ):
##            for j in range( 0 , numberOfSquares ):
##                prev_presence[i][j] = 0
##                prev_presence[numberOfSquares - 1 - i][j] = 0
##        ##blink True

        ##checking whether color of piece is black or white 
        print threshold1
        print threshold2

    return threshold1 , threshold2 , color_square
    
        
        



##checking whether color of piece is black or white 
def check_color( r , c , img ):
    sumt = 0
    for j in range(30):
         for i in range(30):
             sumt = sumt + img.item(int(centres[r][c][1]) - 15 + i , int(centres[r][c][0]) - 15 + j) 
    print r , c, sumt, threshold1, threshold2
    if (r+c)%2==0:
        if sumt < threshold1:
            return -1
        else:
            return 1
    else:
        if sumt > threshold2:
            return 1
        else:
            return -1
##checking whether piece is present or not in a square
def check_presence( image, board):
    for row in range( 8 ):
        for column in range( 8 ):
            roi = image[(corners[row][column][1]+5):(corners[row+1][column+1][1]-5),(corners[row][column][0]+5):(corners[row+1][column+1][0]-5)]
            count = cv2.countNonZero(roi)
            if count > edge_there:
                print row , column
                piece_presence[row][column] = check_color( row , column , board) 
            else:
                piece_presence[row][column] = 0
    return
 
## comparing board positions before and after move is played and determining the move
def find_move(boardPic):
    board_canny = cv2.Canny ( boardPic , min_value , max_value )
    cv2.imwrite( "boardcanny.jpg", board_canny )
    check_presence( board_canny, boardPic)
    counter = 0
    fr = 0
    fc = 0
    ir = 0
    ic = 0
    for i in range( 0 , numberOfSquares ):
        for j in range(0 , numberOfSquares ):
            if not prev_presence[i][j] == piece_presence[i][j]:
                counter=counter+1
                if piece_presence[i][j] == turn : 
                    fr = i
                    fc = j
                else :
                    ir = i
                    ic = j

    print counter
    ## normal move or capture
    if counter == 2 :
        b = [ir , ic , fr , fc ]



    ## en - passent
    elif counter ==3 :
        if turn == 1:
            if not prev_presence[fr - 1][fc - 1] == piece_presence[fr - 1][fc - 1]:
                ir = fr - 1
                ic = fc - 1
                
            else:
                ir = fr - 1
                ic = fc + 1
                
        else :
            if not prev_presence[fr + 1][fc - 1] == piece_presence[fr + 1][fc - 1]:
                ir = fr + 1
                ic = fc - 1
                
            else:
                ir = fr + 1
                ic = fc + 1

        b = [ ir , ic ,fr , fc]

    ## castling
    else :
        if turn == 1 : ##whites turn
            if not prev_presence[0][0] == piece_presence[0][0]:
                b = [ 0 , 4 , 0 , 2 ]
            else :
                b = [ 0 , 4 , 0 , 6 ]
                
        else : ## blacks turn
            if not prev_presence[numberOfSquares - 1][0] == piece_presence[numberOfSquares - 1][0]:
                b = [ numberOfSquares - 1 , 4 , numberOfSquares - 1 , 2 ]
            else :
                b = [ numberOfSquares - 1 , 4 , numberOfSquares - 1 , 6 ]

    return b
    

## updates after determining whether move is legal or not
def update():
    for i in range( 0 , numberOfSquares ):
        for j in range(0 , numberOfSquares):
            previous_presence[i][j] = piece_presence[i][j]
    turn = -turn


#######MAIN CODE

##Start capturing video


board   = cv2.imread( '1206blank.jpg', 0 )
moved   = cv2.imread( '1206infi.jpg' , 0)
threshold1 , threshold2 , color_square = calibrate(board)
print threshold1 , color_square

b = find_move(moved)
print b
print prev_presence
print piece_presence    
""
    ##seek ans from khujau
    #update( ans )
