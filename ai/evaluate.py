def evaluate(board):
    whiteSum = 0
    blackSum = 0
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != 0:
                if piece.color == 0:
                    whiteSum += piece.value + piece.pointsTable[7-row][column]
                else:
                    assert piece.color == 1
                    blackSum += piece.value + piece.pointsTable[row][column]
    return blackSum - whiteSum                    





