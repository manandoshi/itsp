def revertMove(board , move , cap):
    if cap != 0 :
        board[move[0]][move[1]] = board[move[2]][move[3]]
        board[move[2]][move[3]] = cap

    else:
        if board[move[2]][move[3]] == 0:
            print "WUT? :", move
        if board[move[2]][move[3]].name == "K" and abs(move[3] - move[1]) == 2:
            if move[2] == 0 and move[3] == 6:
                 board[0][4] = board[0][6]
                 board[0][6] = 0
                 board[0][7] = board[0][5]
                 board[0][5] = 0
            if move[2] == 0 and move[3] == 2:
                 board[0][4] = board[0][2]
                 board[0][2] = 0
                 board[0][1] = board[0][3]
                 board[0][3] = 0
            if move[2] == 7 and move[3] == 6:
                 board[7][4] = board[7][6]
                 board[7][6] = 0
                 board[7][7] = board[7][5]
                 board[7][5] = 0
            if move[2] == 0 and move[3] == 2:
                 board[7][4] = board[7][2]
                 board[7][2] = 0
                 board[7][1] = board[7][3]
                 board[7][3] = 0 

        else:
            board[move[0]][move[1]] = board[move[2]][move[3]]
            board[move[2]][move[3]] = 0

    return
