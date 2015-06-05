from pygame.locals import *
import pygame

screen = pygame.display.set_mode((1024,768), DOUBLEBUF)
board = pygame.image.load('chess.bmp')
pieces = pygame.image.load('pieces.bmp')
pieces.set_colorkey((0,255,255))
def outp(board):
    while 1:
        screen.blit(board, (0,0))
##      screen.blit(pieces, (0,0),(0,0,50,50))
        for i in range(0,8):
            for j in range(0,8):
                if board[i][j] != "":
                    if board[i][j][0]=="B":
                        r = 50
                    if board[i][j][0]=="W":
                        r = 0
                    if board[i][j][1]=="P":
                        c = 0
                    elif board[i][j][1]=="B":
                        c = 50
                    elif board[i][j][1]=="N":
                        c = 100
                    elif board[i][j][1]=="R":
                        c = 150
                    elif board[i][j][1] == "Q":
                        c = 200
                    elif board[i][j][1] == "K"
                        c = 250

                    screen.blit(pieces, (14 + 50*i,38 + 50*j), (r ,c ,50, 50))

        pygame.display.flip()

