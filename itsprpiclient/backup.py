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
                stepperY.setStepper(move_sequencs[(i*signY)%4])
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
			return 280, 30
		if c == 1:
			return 247, 30
		if c == 2:
			return 213, 33
		if c == 3:
			return 181, 33
		if c == 4:
			return 150, 33
		if c == 5:
			return 122, 36
		if c == 6:
			return 92, 36
		if c == 7:
			return 60, 36

	if r == 1:
		if c == 0:
			return 281, 60
		if c == 1:
			return 251, 63
		if c == 2:
			return 220, 63
		if c == 3:
			return 189, 63
		if c == 4:
			return 157, 65
		if c == 5:
			return 125, 65
		if c == 6:
			return 92, 65
		if c == 7:
			return 60, 68

	if r == 2:
		if c == 0:
			return 279, 92
		if c == 1:
			return 248, 92
		if c == 2:
			return 216, 92
		if c == 3:
			return 185, 94
		if c == 4:
			return 154, 94
		if c == 5:
			return 122, 94
		if c == 6:
			return 91, 94
		if c == 7:
			return 60, 98

	if r == 3:
		if c == 0:
			return 278, 125
		if c == 1:
			return 247, 127
		if c == 2:
			return 216, 127
		if c == 3:
			return 185, 127
		if c == 4:
			return 154, 127
		if c == 5:
			return 123, 127
		if c == 6:
			return 92, 129
		if c == 7:
			return 60, 129

	if r == 4:
		if c == 0:
			return 278, 157
		if c == 1:
			return 245, 157
		if c == 2:
			return 214, 157
		if c == 3:
			return 183, 157
		if c == 4:
			return 152, 159
		if c == 5:
			return 121, 159
		if c == 6:
			return 90, 160
		if c == 7:
			return 59, 160

	if r == 5:
		if c == 0:
			return 277, 188
		if c == 1:
			return 246, 188
		if c == 2:
			return 215, 188
		if c == 3:
			return 184, 190
		if c == 4:
			return 153, 190
		if c == 5:
			return 122, 192
		if c == 6:
			return 90, 192
		if c == 7:
			return 59, 192

	if r == 6:
		if c == 0:
			return 277, 220
		if c == 1:
			return 245, 220
		if c == 2:
			return 213, 220
		if c == 3:
			return 181, 222
		if c == 4:
			return 150, 222
		if c == 5:
			return 119, 222
		if c == 6:
			return 88, 224
		if c == 7:
			return 57, 224

	if r == 7:
		if c == 0:
			return 276, 253
		if c == 1:
			return 245, 253
		if c == 2:
			return 214, 253
		if c == 3:
			return 183, 255
		if c == 4:
			return 152, 255
		if c == 5:
			return 120, 255
		if c == 6:
			return 88, 255
		if c == 7:
			return 57, 255
def xCord(c):
    return 66 + 34*c #X coordinate of c
def yCord(r):
    return 20 + 34*r #y coord of r

def playMove(move):
    
    global board
    theEasyList = ['R', 'B', 'Q', 'P']
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    
    if board[fr][fc] != 0:
        
	x, y = xyCord(fr, fc)
	print "Capture \o/"
	print "Moving emag from ", elecMagnet.x , ",", elecMagnet.y, " to ", x , ",", y
	Move(x - elecMagnet.x, y - elecMagnet.y)
        elecMagnet.on()
	Move(0, 17)
        Move(xCord(-1) - elecMagnet.x, 0)
        Move(0, sink[1] - elecMagnet.y)
        Move(sink[0] - elecMagnet.x, 0)
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
            Move(ic.x - elecMagnet.x, ir.y - elecMagnet.y)
            elecMagnet.on()
            Move(fc.x - elecMagnet.x, 0)
            elecMagnet.off()
            Move(iyR.x - elecMagnet.x, 0)
            elecMagnet.on()
            Move(0, stdVerticalConst)
            Move(fyR.x - elecMagnet.x, 0)
            Move(0, -stdVerticalConst)
    else:
        assert board[ir][ic] == 'N'
        Move(xCord(ic) - elecMagnet.x, yCord(ir) - elecMagnet.y)
        elecMagnet.on()
        if abs(fc-ic) == 1:
            Move(stdHorizontalConst*(fc-ic),0)
            Move(0, yCord(fr)- elecMagnet.y)
            Move(stdHorizontalConst*(fc-ic),0)
        elif abs(fr-ir) == 1:
            Move(0, stdVerticalConst*(fr-ir))
            Move(xCord(fc) - elecMagnet.x, 0)
            Move(stdHorizontalConst*(fc-ic),0)

def updateBoard(move):
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    board[fr][fc] = board[ir][ic]
    prev_presence[fr][fc] = prev_presence[ir][ic]
    board[ir][ic] = 0
    prev_presence[ir][ic] = 0
    if board[ir][ic] == 'K' and abs(fc - ic) == 2:
        if fc==6:
	    prev_presence[ir][5] = prev_presence[ir][7]
	    prev_presence[ir][7] = 0
            board[ir][5], board[ir][7] = 'R', 0
        if fc==2:
	    prev_presence[ir][3] = prev_presence[ir][0]
	    prev_presence[ir][0] = 0
            board[ir][3], board[ir][0] = 'R' , 0
    

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
            assert True
		#retraceMove()
    updateBoard(move)
    return end

def receiveMove():
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))
    playMove(move)
    updateBoard(move) 
    return move[4]
    

server = socket.socket()
host = "127.0.0.1"
port = 8888
print "fu",
server.connect((host, port))
print "ck"

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

