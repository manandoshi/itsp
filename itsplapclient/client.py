import socket
import graphics

host = '192.168.0.112'
port = input("Port:")

s = socket.socket()
s.connect((host,port))

p = int(s.recv(1024)) - 1
print "Yay. Player ",  p
turn = 0

board = [[ 'WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR'],
         [ 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
         [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ],
         [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ],
         [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ],
         [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ],
         [ 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
         [ 'BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']]

graphics.outp(board)
GameOver = False

while not GameOver:
    if( turn == p ):
        print "my turn \o/"
        end = False
        while not end:
            inp = graphics.inpt(board)
            print "sending Move..."
            s.send(inp)
            print "Move sent"
            feedback = s.recv(1024)
            print "Feedback :", feedback
            end = False if feedback=="False" else True

            if feedback == "End":
                GameOver=True

        inp = int(inp)
        ir = inp/1000
        ic = (inp/100)%10
        fr = (inp/10)%10
        fc = inp%10
        board[fr][fc] = board[ir][ic]
        board[ir][ic] = 0
        
        if board[fr][fc][1] == "K":
            if abs(ic-fc)==2:
                if fc==6:
                    board[ir][5], board[ir][7] = board[ir][7], 0
                if fc==2:
                    board[ir][3], board[ir][0] = board[ir][0] , 0
        graphics.outp(board)
        if GameOver:
            print "I WON"
            # I won
    
    else:
        print " Not my turn. Listening for input: "
        inp = s.recv(1024)
        print " Got ze input :" , inp
        
        strInput = inp[:4]
        print "Move part :", strInput

        end = inp[4]
        print "End prt : ", end
        inp = int(strInput)
        
        ir = inp/1000
        ic = (inp/100)%10
        fr = (inp/10)%10
        fc = inp%10

        board[fr][fc] = board[ir][ic]
        board[ir][ic] = 0
        if board[fr][fc][1] == "K":
            if abs(ic-fc)==2:
                if fc==6:
                    board[ir][5], board[ir][7] = board[ir][7], 0
                if fc==2:
                    board[ir][3], board[ir][0] = board[ir][0] , 0
        
        if GameOver:
            print "I WON"
        graphics.outp(board)
        
        if end!="0":
            if end == "3":
                assert True
                #DRAW
            else:
                assert True
                #ILOSE
            GameOver = True
    
    turn = 1 - turn

s.close()
