import cv2
import numpy as np
import time
from math import *
import RPi.GPIO as GPIO
##number of squares in chessboard
numberOfSquares = 8

cap = cv2.VideoCapture(0)
##determines whose turn it is
turn = 1
cam = 17
##min value for canny-threshold
min_value = 50
##max value for canny-threshold
max_value = 70

## an array having the x and y coordinate of the cornersof the chessboard
corners = [[[0 for a in range(2)] for a in range(numberOfSquares + 1)]for a in range(numberOfSquares + 1)]

##an array having the x and y coordinates of the centres of the chessboard
centres = [[[0 for a in range(2)] for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board after the move is played
piece_presence = [[0 for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##an array storing the structure of the board before the move is played
prev_presence  = [[0 for a in range(numberOfSquares)]for a in range(numberOfSquares)]

##Dimension of square whose region to be checked for color detection
color_square = 10.0

##count for edge_detection
edge_there = 50


##side of square
square_side = 0

##ratio of side of square to piece
factor = 3
factor_for_t1 = 0.75
factor_for_t2 = 0.8

#### determines threshold for checking color of piece 
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

def photoClick(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
            if not GPIO.input(pin):
		for i in range(24):
			ret, frame = cap.read()
			time.sleep(1.0/24.0)
		ret, frame = cap.read()
		return ret, frame
            
def flipH(arr):
	ret = [[[0 for a in range(2)]for b in range(9)]for c in range(9)]
	for i in range(9):
		for j in range(9):
			ret[i][j][0] = arr[i][8-j][0]
			ret[i][j][1] = arr[i][8-j][1]
	return ret

def flipV(arr):
	ret = [[[0 for a in range(2)]for b in range(9)]for c in range(9)]
	for i in range(9):
		for j in range(9):
			ret[i][j][0] = arr[8-i][j][0]
			ret[i][j][1] = arr[8-i][j][1]
	return ret

def flipD(arr):
	ret = [[[0 for a in range(2)]for b in range(9)]for c in range(9)]
	for i in range(9):
		for j in range(9):
			ret[i][j][0] = arr[j][i][0]
			ret[i][j][1] = arr[j][i][1]
	return ret

##function sets the initial conditions at the start of play
def calibrate():
    global cam
    ##blink false
    global threshold1
    global threshold2
    global color_square
    global square_side
    global corners
    print "Waiting for button"
    while 1:
	    i = 1
	    ret , img = photoClick(cam)
	    print "Button pushed"
	    print img
	    patternsize = (numberOfSquares + 1, numberOfSquares + 1)
	    corn = cv2.findChessboardCorners( img, patternsize )
	    cv2.drawChessboardCorners( img, (9,9), corn[1], corn[0])
	    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    print corn[0]
	    print corn[1]

	    if corn[0]:
	    	    cv2.imwrite('cyay.jpg',img)
		    print "YAY. Calib done"
		    break
	    else:
		    print "Calib not done. Saving image"
		    cv2.imwrite("cfail.jpg",img)
    if corn[0]:
        number = 0
        ##calibrating the corners array
        for i in range( 0 , numberOfSquares + 1 ):
            for j in range( 0 , numberOfSquares + 1 ):
                corners[ i ][ j ][ 0 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 0 ]
                corners[ i ][ j ][ 1 ] = corn[ 1 ][ (numberOfSquares + 1)*i+j, 0, 1 ]
                number = number + 1
                print corners[i][j]
                print number
	
	for i in range(4):
		if corners[0][0][0] < 320 and corners[0][0][1]<240:
			break
		if i == 1:
			corners = flipH(corners)
		if i == 2:
			corners = flipV(corners)
		if i == 3:
			corners = flipH(corners)
	
	if corners[0][8][0] > 320 and corners[0][8][1] < 240:
		assert True
	else:
		corners = flipD(corners)
        x_difference = corners[4][4][0] - corners[4][5][0] 
        y_difference = corners[4][4][1] - corners[4][5][1]
        square_side = sqrt( x_difference*x_difference + y_difference*y_difference)
        print "Square side: " , square_side 
        ##calibrating the centres array        
        for i in range( 0 , numberOfSquares ):
            for j in range( 0 , numberOfSquares ):
                centres[ i ][ j ][ 0 ] = (corners[ i ][ j ][ 0 ] + corners[ i+1 ][ j ][ 0 ] + corners[ i ][ j+1 ][ 0 ] + corners[ i+1 ][ j+1 ][ 0 ])/4
                centres[ i ][ j ][ 1 ] = (corners[ i ][ j ][ 1 ] + corners[ i+1 ][ j ][ 1 ] + corners[ i ][ j+1 ][ 1 ] + corners[ i+1 ][ j+1 ][ 1 ])/4
                
        color_square = (square_side / factor)
        
        threshold1 = threshold_black_in_white(centres , img , color_square)
        threshold2 = threshold_white_in_black(centres , img , color_square)

        ##setting up initial structure of pieces 
        for i in range( 0 , 2 ):
            for j in range( 0 , numberOfSquares ):
                prev_presence[i][j] = 1
                prev_presence[numberOfSquares - 1 - i][j] = -1
        ##blink True

        ##checking whether color of piece is black or white
        threshold1 = threshold1*factor_for_t1
        threshold2 = threshold2*factor_for_t2
        print threshold1
        print threshold2

    #return threshold1 , threshold2 , color_square

##checking whether color of piece is black or white 
def check_color( r , c , img ):
    sumt = 0
    for j in range(int(color_square)):
         for i in range(int(color_square)):
             sumt = sumt + img.item(int(centres[r][c][1]) - color_square/2 + i , int(centres[r][c][0]) - color_square/2 + j) 
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
def check_presence( image, boardPic):
    for row in range( 8 ):
        for column in range( 8 ):
	    print "row:", row, "column:", column
            roi = image[(corners[row][column][1]+7):(corners[row+1][column+1][1]-7),(corners[row][column][0]+7):(corners[row+1][column+1][0]-7)]
	    #print "ROI: ", roi
	    count = cv2.countNonZero(roi) 
	    print "Count value:", count
	    
	    if count > edge_there:
                piece_presence[row][column] = check_color( row , column , boardPic) 
            else:
                piece_presence[row][column] = 0
    return
 
## comparing board positions before and after move is played and determining the move
def find_move(boardPic):
    boardPic = cv2.cvtColor(boardPic,cv2.COLOR_BGR2GRAY)
    board_canny = cv2.Canny ( boardPic , min_value , max_value )
    cv2.imwrite( "boardpic.jpg", boardPic)
    cv2.imwrite( "canny.jpg", board_canny )
    check_presence( board_canny, boardPic)
    print "piece pres:"
    print piece_presence
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
        b = [ir , 7 - ic , fr , 7 - fc ]

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

        b = [ ir , 7 - ic ,fr , 7 - fc]

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
def update(turn , ans):
    if ans == True:
        for i in range( 0 , numberOfSquares ):
            for j in range(0 , numberOfSquares):
                prev_presence[i][j] = piece_presence[i][j]
        turn = -turn
        return turn



