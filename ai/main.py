from chess import *
import socket
import ai

def receiveMove():
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))
    updateBoard(move) 
    return move[4]
    
def sendMove(move):
    end = 0
    moveString = str(move[0]) + str(move[1]) + str(move[2]) + str(move[3])
    server.send(moveString)
    message = server.recv(1024)
    updateBoard(move)
    return end

server = socket.socket()
host = '127.0.0.1'
port = 5001

server.connect((host,port))

board = initBoard()

playerID = int(server.recv(1024)) - 1
pTurn = 0
end = False

while not end:
    if pTurn == playerID:
        move = ai.playMove(board, pTurn)
        sendMove(move)
    else:
        state = receiveMove()
	if state:
            end = True
           if state == playerID + 1:
                #Tell player he won
                assert True
                return
            if state == 3:
                #Tell player he drew
                assert True
                return
            else:
                assert True
                return
                #Tell player he lost
    pTurn = 1 - pTurn
s.close()
