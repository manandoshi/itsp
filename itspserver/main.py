from chess import *
from inp import *
import socket

def initSocket(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(2)
    print "Waiting for 2 connections :" 
    p1 , addr1 = s.accept()
    print "Connected to p1(",addr1,")"
    p2, addr2 = s.accept()
    print "Connected to p2(",addr2,")"
    p1.send('1')
    p2.send('2')
    return p1, p2

def main():

    end = False
    playerTurn = 0
    
    p = initSocket(5001)
    board = []
    board = initBoard()
    
    prnt(board)
    
    while not end:
        stringInput = inp(p, playerTurn)
        intInput = int(stringInput)
        inputArray = [ intInput/1000 , (intInput/100)%10 , (intInput/10)%10 , intInput%10 ]
        
        print "Got input ", inputArray , " from player ", playerTurn
        
        end, err = mv(board, inputArray , playerTurn)
        
        outpfeedback(err, playerTurn, p, end)
        
        if not err:
            print "Move played"
            playerTurn = 1 - playerTurn
            print "END: " + str(end)
            print stringInput + str(end)
            outp(stringInput + str(end), p, playerTurn)
            prnt(board)
    p[0].close()
    p[1].close()
    return
if __name__ == '__main__':
    main()
