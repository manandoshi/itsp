import RPi.GPIO as GPIO
import time
import socket

GPIO.setmode(GPIO.BCM)

sink = ("""sink coords""")

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
    def _init__(self, control):
        self.control = control
        GPIO.setup(self.control, GPIO.OUT)
        self.x, self.y = 0
    def on():
        GPIO.output(self.control, 1)
    def off():
        GPIO.output(self.control, 0)
    def move(x,y):
        self.x += x
        self.y += y

stepperX = stepper("""Pins""")
stepperY = stepper("""Pins""")
elecMagnet = magnet("""Pin""")

def Move(x,y):
    stepperX.setSteps(x)
    stepperY.setSteps(y)
    elecMagnet.move(x,y)
    move_sequence = ((1,0,0,0),(0,0,1,0),(0,1,0,0),(0,0,0,1))
    try:
        signX, signY = (abs(stepperX.steps)/stepperX.steps), (abs(stepperY.steps)/stepperY.steps)
        stepperX.setSteps(signX*stepperX.steps)
        stepperY.setSteps(signY*stepperY.steps)
        counterX, counterY = 0, 0
        delay = 0.0055/min(stepperX.steps, stepperY.steps)
        for i in range(stepperX.steps*stepperY.steps*4):
            if (i+1)%stepperX.steps == 0:
                stepperY.setStepper(move_sequence[counterY%4*signY])
                counterY+=1
            if (i+1)%stepperY.steps == 0:
                stepperX.setStepper(move_sequence[counterX%4*signX])
                counterX+=1
            time.sleep(delay)
    except ZeroDivisionError:
        stepper = stepperX if stepperX.steps != 0 else stepperY
        sign = abs(stepper.steps)/stepper.steps
        stepper.setSteps(sign*stepper.steps)
        counter = 0
        delay = 0.0055
        for i in range(stepper.steps*4):
            stepper.setStepper(move_sequence[counter%4*sign])         
            counter+=1
            time.sleep(delay)

def playMove(move):
    theEasyList = ['R', 'B', 'Q', 'P']
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    if board[fr][fc] != 0:
        Move(fc.x - elecMagnet.x, fr.y - elecMagnet.y)
        elecMagnet.on()
        Move(0, stdVerticalConst)
        Move(someEdgeCol.x - elecMagnet.x, 0)
        Move(0, sink.y - elecMagnet.y)
        Move(sink.x - elecMagnet.x, 0)
        elecMagnet.off()
        
    if board[ir][ic] in theEasyList:
        Move(ic.x - elecMagnet.x, ir.y - elecMagnet.y)
        elecMagnet.on()
        Move(fc.x - elecMagnet.x, fr.y - elecMagnet.y)
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
        Move(ic.x - elecMagnet.x, ir.y - elecMagnet.y)
        elecMagnet.on()
        if abs(fc-ic) == 1:
            Move(stdHorizontalConst*(fc-ic),0)
            Move(0, fr.y - elecMagnet.y)
            Move(stdHorizontalConst*(fc-ic),0)
        elif abs(fr-ir) == 1:
            Move(0, stdVerticalConst*(fr-ir))
            Move(fc.x - elecMagnet.x, 0)
            Move(stdHorizontalConst*(fc-ic),0)

def updateBoard(move):
    ir, ic, fr, fc = move[0], move[1], move[2], move[3]
    board[fr][fc] = board[fr][fc]
    board[ir][ic] = 0
    if board[ir][ic] == 'K' and abs(fc - ic) == 2:
        if fc==6:
            board[ir][5], board[ir][7] = 'R', 0
        if fc==2:
            board[ir][3], board[ir][0] = 'R' , 0
    

def sendMove():
    sentValid = False
    while not sentValid:
        move = #ImgProc
        server.send(move)
        message = server.recv(1024)
        if message = 'True':
            sentValid = True
        elif message = 'False':
            sentValid = False11
        if not sentValid:
            #retraceMove()
    updateBoard(move)

def receiveMove():
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))
    updateBoard(move)
    return move[4]
    playMove(move)

server = socket.socket()
host =
port =
server.connect((host, port))
board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
         ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
playeridInt = int(server.recv(1024))
if playeridInt == 1:
    playeridStr = 'white'
elif playeridInt == 2:
    playeridStr = 'black'
move = 
if playeridStr == 'white':
    sendMove(sock)
while 1:
    end = int(receiveMove(sock))
    if end:
        break
    sendMove(sock)




    
