import RPi.GPIO as GPIO
import time
import socket
from image_processing import *

#init
cal = 17
cam = 17

GPIO.setmode(GPIO.BCM)
cap = cv2.VideoCapture(0)


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
        self.x, self.y = 0
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

def Move(x,y):
    y = -y
    stepperX.setSteps(x)
    stepperY.setSteps(y)
    elecMagnet.move(x,y)
    move_sequence = ((1,0,0,0),(0,0,0,1),(0,1,0,0),(0,0,1,0))
    try:
        signX, signY = (abs(stepperX.steps)/stepperX.steps), (abs(stepperY.steps)/stepperY.steps)
        stepperX.setSteps(signX*stepperX.steps)
        stepperY.setSteps(signY*stepperY.steps)
        if (abs(x) == abs(y)):
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


def xCord(c):
    return 66 + 34*c #X coordinate of c
def yCord(r):
    return 20 + 34*c #y coord of r

def playMove(move):
    theEasyList = ['R', 'B', 'Q', 'P']
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    if board[fr][fc] != 0:
        Move(xCord(fc) - elecMagnet.x, yCord(fr) - elecMagnet.y)
        elecMagnet.on()
        Move(0, 17)
        Move(xCord(-1) - elecMagnet.x, 0)
        Move(0, sink[1] - elecMagnet.y)
        Move(sink[0] - elecMagnet.x, 0)
        elecMagnet.off()
        
    if board[ir][ic] in theEasyList:
        Move(xCord(ic) - elecMagnet.x, yCord(ir) - elecMagnet.y)
        elecMagnet.on()
        Move(xCord(fc) - elecMagnet.x, yCord(fr) - elecMagnet.y)
        elecMagnet.off()
    elif board[ir][ic] == 'K':
        if abs(fc - ic) != 2:
            Move(ic.x - elecMagnet.x, ir.y - elecMagnet.y)
            elecMagnet.on()
            Move(fc.x - elecMagnet.x, fr.y - elecMagnet.y)
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
    board[fr][fc] = board[fr][fc]
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
            sentValid = False
        elif message == 'End':
            sentValid = True
            end = 1
        if not sentValid:
            #retraceMove()
    updateBoard(move)
    return end

def receiveMove():
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))
    updateBoard(move)
    move[0] = 7*playerID + move[0]*((-1)**playerID)
    move[2] = 7*playerID + move[2]*((-1)**playerID)
    playMove(move)
    return move[4]
    

server = socket.socket()
host = "192.168.0.141"
port = 5000
server.connect((host, port))


board = [['R','N','B','Q','K','B','N','R'],
         ['P','P','P','P','P','P','P','P'],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
         ['P','P','P','P','P','P','P','P'],
         ['R','N','B','Q','K','B','N','R']]

##Calibrate :(
calibrate()

playerID = int(server.recv(1024)) - 1

sink = (7*playerID-0,0)

##Tell player his color
##Set board

pTurn = 0
end = False
while not end:
    if pTurn == playerID:
        ret, boardPic = photoClick(cam)
        sendMove(boardPic)
        pTurn = 1 - pTurn
    else:
        state = receiveMove()
        if not state:
            end = True
            if state = playerID + 1:
                #Tell player he won
                assert True
            if state = 3:
                #Tell player he drew
                assert True
            else:
                assert True
                #Tell player he lost
##Go to 0,0
s.close()
##other losing stuff
