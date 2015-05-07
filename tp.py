import socket
import RPi.GPIO as GPIO
import time

##GPIO init:
GPIO.setmode(GPIO.BCM)
Xpins = (25, 23, 18, 15)
Ypins = (12, 16, 20, 21)

for i in Xpins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 0)
for i in Ypins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 0)

##Socket init
host = "0.0.0.0"
port = 9889

s = socket.socket()

s.bind((host,port))
s.listen(1)

c,addr = s.accept()

end = False

c.send("Connected to RPi...")

##Stepper init
moveseq = ((1,0,0,0),(0,0,1,0),(0,1,0,0),(0,0,0,1))
delay = 0.0055

def setSteps(pins, values):
    for i in range(0,4):
        GPIO.output(pins[i], values[i])
##Xmove: move stepperX by steps
def xmove(steps):
    steps = int(steps)
    sign = steps/abs(steps)
    for i in range(0,abs(steps*4)):
        setSteps(Xpins, moveseq[(sign*i)%4])
	time.sleep(delay)
    setSteps(Xpins,(0,0,0,0))
def ymove(steps):
    steps = int(steps)
    sign = steps/abs(steps)
    for i in range(0,abs(steps*4)):
	setSteps(Ypins, moveseq[(sign*i)%4])
	time.sleep(delay)
    setSteps(Ypins,(0,0,0,0))
    
while not end:
    c.send("X steps: ")
    stepx = c.recv(1024)
    if stepx:
        xmove(stepx)
    c.send("Y steps: ")
    stepy = c.recv(1024)
    if stepy:
        ymove(stepy)
    c.send("Wanna continue? (y/n)")
    end = True if c.recv(1024) == "n" else False

s.close()
