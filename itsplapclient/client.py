import socket
import graphics

host = '127.0.0.1'
port = 5000

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
        board[(inp/10)%10][inp%10] = board[inp/1000][(inp/100)%10]
        board[inp/1000][(inp/100)%10] = 0
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

        board[(inp/10)%10][inp%10] = board[inp/1000][(inp/100)%10]
        board[inp/1000][(inp/100)%10] = 0
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
