from pygame.locals import *
import pygame

screen = pygame.display.set_mode((424,469), DOUBLEBUF)
boardSurface = pygame.image.load('chess.bmp')

pieces = pygame.image.load('pieces.bmp')
pieces.set_colorkey((0,255,255))

box = pygame.image.load('box.bmp')
box.set_colorkey((0,255,255))

def outp(board):
    screen.blit(boardSurface, (0,0))
##      screen.blit(pieces, (0,0),(0,0,50,50))
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] != 0:
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
                elif board[i][j][1] == "K":
                    c = 250

                screen.blit(pieces, (14 + 50*j , 388 - 50*i), (c ,r ,50, 50))

    pygame.display.flip()

def inpt(board):
    print "Debug : Entered inpt"
    p = (0,0)
    c = 0
    m = [0,0,0,0]
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Q"

            if event.type == pygame.MOUSEBUTTONUP:
                p = pygame.mouse.get_pos()
                print "Debug p: ", p 
                if c == 0:
                    if p[0] > 14 and p[0] < 414 and p[1] > 38 and p[1] < 438 :
                        m[0] = 7 - ((p[1] - 38)/50)
                        m[1] = ((p[0] - 14) / 50)
                        print " First click:" , m
                        c = 1
                        screen.blit(box, (14 + 50*m[1], 388 - 50*m[0]),(0,0,50,50))
                        
                elif c == 1:
                    if p[0] > 14 and p[0] < 414 and p[1] > 38 and p[1] < 438 :
                        m[2] = (7 - (p[1] - 38)/50)
                        m[3] = ((p[0] - 14) / 50)
                        if m[0] == m[2] and m[1] == m[3] :
                            m = [0,0,0,0]
                            c = 0
                            outp(board)
                        else:
                            print "Debug m:" , m
                            return str(m[0]) + str(m[1]) + str(m[2]) + str(m[3])
