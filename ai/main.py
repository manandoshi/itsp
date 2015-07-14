from chess import *
import socket
import ai

def receiveMove(board):
    recvdMove = server.recv(1024)
    move = []
    for pos in recvdMove:
        move.append(int(pos))
    updateBoard(move, board) 
    return move[4]
    
def sendMove(move,board):
    end = 0
    moveString = str(move[0]) + str(move[1]) + str(move[2]) + str(move[3])
    server.send(moveString)
    message = server.recv(1024)
    updateBoard(move, board)
    return end

server = socket.socket()
host = '127.0.0.1'
port = input("Port: ")

server.connect((host,port))

board = initBoard()

playerID = int(server.recv(1024)) - 1
pTurn = 0
end = False

while not end:
    if pTurn == playerID:
        move = ai.playMove(board, pTurn)
        sendMove(move, board)
    else:
        state = receiveMove(board)
	if state:
            end = True
            if state == playerID + 1:
                break
            if state == 3:
                break
            else:
                break
    pTurn = 1 - pTurn
s.close()
