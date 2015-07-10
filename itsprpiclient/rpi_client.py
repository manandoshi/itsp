import RPi.GPIO as GPIO
import time
import socket
from image_processing import *

#init
#cal = 17
#cam = 17

sink = (0,0)
GPIO.setmode(GPIO.BCM)

board = [[0 for a in range(8)]for b in range(8)]
"""
GPIO.setup(calFeedbackFalse, GPIO.OUT)
GPIO.setup(calFeedbackTrue, GPIO.OUT)
GPIO.setup(camFeedbackFalse, GPIO.OUT)

GPIO.setup(GameEndWin, GPIO.OUT)
GPIO.setup(GameEndLose, GPIO.OUT)
GPIO.setup(GameEndDraw, GPIO.OUT)
"""

class stepper():
    def __init__(self, A1, A2, B1, B2):
        self.A1 = A1
        self.A2 = A2
        self.B1 = B1
        self.B2 = B2
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.B1, GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)
        
    def setSteps(self, steps):
        self.steps = steps
        
    def setStepper(self, (w1, w2, w3, w4)):
        GPIO.output(self.A1, w1)
        GPIO.output(self.A2, w2)
        GPIO.output(self.B1, w3)
        GPIO.output(self.B2, w4)

class magnet():
    def __init__(self, control):
        self.control = control
        GPIO.setup(self.control, GPIO.OUT)
        self.x, self.y = 0, 0
    def on(self):
        GPIO.output(self.control, 1)
    def off(self):
        GPIO.output(self.control, 0)
    def move(self,x,y):
        self.x += x
        self.y += y

stepperX = stepper(12,16,20,21)
stepperY = stepper(25,23,18,15)
elecMagnet = magnet(14) #fix
elecMagnet.off()

def Move(x,y):
    y = -y
    stepperX.setSteps(x)
    stepperY.setSteps(y)
    move_sequence = ((1,0,0,0),(0,0,0,1),(0,1,0,0),(0,0,1,0))
    try:
        signX, signY = (abs(stepperX.steps)/stepperX.steps), (abs(stepperY.steps)/stepperY.steps)
        stepperX.setSteps(signX*stepperX.steps)
        stepperY.setSteps(signY*stepperY.steps)
        if (abs(x) == abs(y)):
    	    elecMagnet.move(x,-y)
	    delay = 0.0055    
            for i in range(abs(x)*4):
                stepperX.setStepper(move_sequence[(i*signX)%4])
                time.sleep(delay)
                stepperX.setStepper((0,0,0,0))
                stepperY.setStepper(move_sequence[(i*signY)%4])
                time.sleep(delay)
                stepperY.setStepper((0,0,0,0))
	else:
            Move(x,0)
            Move(0,-y)
    except ZeroDivisionError:
	if x==0 and y==0:
	    return
        
        elecMagnet.move(x,-y)
	stepper = stepperX if stepperX.steps != 0 else stepperY
        sign = abs(stepper.steps)/stepper.steps
        stepper.setSteps(sign*stepper.steps)
        counter = 0
        delay = 0.0055*2
        for i in range(stepper.steps*4):
            stepper.setStepper(move_sequence[(counter*sign)%4])         
            counter+=1
            time.sleep(delay)
	stepper.setStepper((0,0,0,0))

def xyCord(r,c):
	if r == 0:
		if c == 0:
			return 280, 16
		if c == 1:
			return 250, 16
		if c == 2:
			return 220, 16
		if c == 3:
			return 189, 16
		if c == 4:
			return 158, 16
		if c == 5:
			return 127, 16
		if c == 6:
			return 95, 16
		if c == 7:
			return 65, 16

	if r == 1:
		if c == 0:
			return 280, 47
		if c == 1:
			return 250, 47
		if c == 2:
			return 220, 47
		if c == 3:
			return 189, 47
		if c == 4:
			return 158, 47
		if c == 5:
			return 127, 47
		if c == 6:
			return 95, 47
		if c == 7:
			return 64, 47

	if r == 2:
		if c == 0:
			return 280, 79
		if c == 1:
			return 250, 79
		if c == 2:
			return 219, 79
		if c == 3:
			return 188, 79
		if c == 4:
			return 157, 79
		if c == 5:
			return 126, 79
		if c == 6:
			return 95, 79
		if c == 7:
			return 64, 79

	if r == 3:
		if c == 0:
			return 279, 110
		if c == 1:
			return 249, 110
		if c == 2:
			return 219, 110
		if c == 3:
			return 188, 110
		if c == 4:
			return 157, 110
		if c == 5:
			return 126, 110
		if c == 6:
			return 94, 110
		if c == 7:
			return 63, 110

	if r == 4:
		if c == 0:
			return 279, 142
		if c == 1:
			return 249, 142
		if c == 2:
			return 218, 142
		if c == 3:
			return 187, 142
		if c == 4:
			return 156, 142
		if c == 5:
			return 125, 141
		if c == 6:
			return 93, 141
		if c == 7:
			return 62, 141

	if r == 5:
		if c == 0:
			return 278, 173
		if c == 1:
			return 248, 173
		if c == 2:
			return 218, 173
		if c == 3:
			return 187, 173
		if c == 4:
			return 156, 173
		if c == 5:
			return 124, 173
		if c == 6:
			return 92, 172
		if c == 7:
			return 61, 172

	if r == 6:
		if c == 0:
			return 278, 205
		if c == 1:
			return 248, 205
		if c == 2:
			return 217, 205
		if c == 3:
			return 186, 205
		if c == 4:
			return 155, 205
		if c == 5:
			return 124, 204
		if c == 6:
			return 92, 204
		if c == 7:
			return 61, 204

	if r == 7:
		if c == 0:
			return 277, 236
		if c == 1:
			return 247, 236
		if c == 2:
			return 217, 236
		if c == 3:
			return 186, 236
		if c == 4:
			return 154, 236
		if c == 5:
			return 123, 235
		if c == 6:
			return 91, 235
		if c == 7:
			return 60, 235

def playMove(move):
    
    elecMagnet.off()
    global board
    theEasyList = ['R', 'P']
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    
    if board[fr][fc] != 0:
        
	x, y = xyCord(fr, fc)
	print "Capture \o/"
	print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	Move(x - elecMagnet.x, y - elecMagnet.y)
        elecMagnet.on()

	x1, y1 = xyCord(ir,ic)
	x2, y2 = xyCord(ir-1,ic)

	yd = (y2-y1)/2
	Move(0, yd)
	xs,ys = xyCord(ir,ic)
	Move(20 - elecMagnet.x,0)

        #Move(xCord(-1) - elecMagnet.x, 0)
        #Move(0, sink[1] - elecMagnet.y)
        #Move(sink[0] - elecMagnet.x, 0)
        
	elecMagnet.off()
    
    if board[ir][ic] in theEasyList:
	x, y = xyCord( ir, ic)
	print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
        Move(x - elecMagnet.x, y - elecMagnet.y)
        elecMagnet.on()
	x, y = xyCord( fr, fc)
	print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
        Move(x - elecMagnet.x, y - elecMagnet.y)
        elecMagnet.off()
    elif board[ir][ic] == 'B':
	irs, ics = xyCord(ir, ic)
	frs, fcs = xyCord(fr,fc)
	d = min(abs(frs-irs),abs(fcs-ics))
	 
	signR = (fr-ir)/abs(fr-ir)
	signC = (ic-fc)/abs(fc-ic)
	
	x, y = xyCord(ir, ic)
	 
	print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	Move(x-elecMagnet.x, y-elecMagnet.y)
	
	elecMagnet.on()
	print "Moving by ", signR*d, ", " , signC*d 
	Move(signC*d,signR*d)
	x, y = xyCord(fr, fc)
	Move(x - elecMagnet.x, y - elecMagnet.y)
	#Move((fr-ir)-(signR*d), (fc-ic)-(signC*d))
	elecMagnet.off()
    elif board[ir][ic] == 'Q':
	
	irs, ics = xyCord(ir, ic)
	frs, fcs = xyCord(fr,fc)
	
	if abs(fcs - ics)>15 and abs(frs-irs)>15:
		
	    d = min(abs(frs-irs),abs(fcs-ics))
	     
	    signR = (fr-ir)/abs(fr-ir)
	    signC = (ic-fc)/abs(fc-ic)
	    
	    x, y = xyCord(ir, ic)
	    
	    print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	    Move(x-elecMagnet.x, y-elecMagnet.y)
	    
	    elecMagnet.on()
	    print "Moving by ", signR*d, ", " , signC*d 
	    Move(signC*d,signR*d)
	    x, y = xyCord(fr, fc)
	    Move(x - elecMagnet.x, y - elecMagnet.y)
	    #Move((fr-ir)-(signR*d), (fc-ic)-(signC*d))
	else:
	    x, y = xyCord( ir, ic)
	    print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	    Move(x - elecMagnet.x, y - elecMagnet.y)
	    elecMagnet.on()
	    x, y = xyCord( fr, fc)
	    print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	    Move(x - elecMagnet.x, y - elecMagnet.y)
	    elecMagnet.off()
    elif board[ir][ic] == 'K':
        if abs(fc - ic) != 2:
            x, y = xyCord(ir,ic)
	    Move(x - elecMagnet.x, y - elecMagnet.y)
            elecMagnet.on()
	    x, y = xyCord(fr,fc)
            Move(x - elecMagnet.x, y - elecMagnet.y)
            elecMagnet.off()
        else:
            iyR = 7 if fc - ic > 0 else 0
            fyR = 5 if fc - ic > 0 else 3
            xi, yi = xyCord( ir, ic)
	    xf, yf = xyCord( fr, fc)
	    iRx, iRy = xyCord( ir, iyR )
	    fRx, fRy = xyCord( fr, fyR )
	    Move(xi - elecMagnet.x, yi - elecMagnet.y)
            elecMagnet.on()
            Move(xf - elecMagnet.x, yf - elecMagnet.y)
            elecMagnet.off()
            Move(iRx - elecMagnet.x, 0)
            elecMagnet.on()
            Move(0, 30)
            Move(fRx - elecMagnet.x, 0)
            Move(0, -30)
	    elecMagnet.off()
    else:
        assert board[ir][ic] == 'N'
	xi, yi = xyCord(ir,ic)
	xf, yf = xyCord(fr, fc)
        Move(xi - elecMagnet.x, yi - elecMagnet.y)
        elecMagnet.on()
        if abs(fc-ic) == 1:
	    stdHorizontalConst = abs(xi - xf)/2
            Move(stdHorizontalConst*(ic-fc),0)
            Move(0, yf - elecMagnet.y)
            Move(stdHorizontalConst*(ic-fc),0)
        elif abs(fr-ir) == 1:
	    stdVerticalConst = abs(yf - yi)/2
            Move(0, stdVerticalConst*(fr-ir))
            Move(fcs - elecMagnet.x, 0)
            Move(stdHorizontalConst*(fc-ic),0)
	elecMagnet.off()

def updateBoard(move):
    global prev_presence
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    board[fr][fc] = board[ir][ic]
    prev_presence[fr][7-fc] = prev_presence[ir][7-ic]
    board[ir][ic] = 0
    prev_presence[ir][7-ic] = 0
    if board[ir][ic] == 'K' and abs(fc - ic) == 2:
        if fc==6:
	    prev_presence[ir][2] = prev_presence[ir][0]
	    prev_presence[ir][0] = 0
            board[ir][5], board[ir][7] = 'R', 0
        if fc==2:
	    prev_presence[ir][4] = prev_presence[ir][7]
	    prev_presence[ir][7] = 0
            board[ir][4], board[ir][7] = 'R' , 0
    

def sendMove(boardPic):
    end = 0
    sentValid = False
    while not sentValid:
        move = find_move(boardPic)
        moveString = str(move[0]) + str(move[1]) + str(move[2]) + str(move[3])
        server.send(moveString)
        message = server.recv(1024)
        if message == 'True':
            sentValid = True
        elif message == 'False':
            sentValid = True
	    ##^SET THIS TO FALSE^##
        elif message == 'End':
            sentValid = True
            end = 1
        if not sentValid:
            print "Invalid move. retry"
	    boardPic = photoClick(cam)
		#retraceMove()
    updateBoard(move)
    return end

def receiveMove():
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))

    move[0] = move[0]*((-1)**playerID)+(7*playerID)
    move[2] = move[2]*((-1)**playerID)+(7*playerID)
    playMove(move)
    updateBoard(move) 
    return move[4]
    

server = socket.socket()
host = "127.0.0.1"
port = 5001
server.connect((host, port))

board = [['R','N','B','Q','K','B','N','R'],
         ['P','P','P','P','P','P','P','P'],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         ['P','P','P','P','P','P','P','P'],
         ['R','N','B','Q','K','B','N','R']]

##Calibrate :(
print "About to calib"
calibrate()

playerID = int(server.recv(1024)) - 1

if playerID == 1:
    flipH(corners,9)
    flipH(centres,8)

##Tell player his color
##Set board

pTurn = 0
end = False
while not end:
    if pTurn == playerID:
        print "My Turn. Taking pic..."
	ret, boardPic = photoClick(cam)
	print "Ret:",ret
        sendMove(boardPic)
        pTurn = 1 - pTurn
    else:
	print "Not my turn."
        state = receiveMove()
	print "State:" , state
        pTurn = 1-pTurn
	if state:
            end = True
            if state == playerID + 1:
                #Tell player he won
                assert True
            if state == 3:
                #Tell player he drew
                assert True
            else:
                assert True
                #Tell player he lost
##Go to 0,0
s.close()
##other losing stuff

