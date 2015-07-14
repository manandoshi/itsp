from chess import *
from revert import *
from evaluate import *

def getVal(level, parentVal, typ, board):
    if level == 3:
        value = evaluate(board)
        return value, (0,0,0,0)
    dVal = typ*-90000
    c = 0 if typ == -1 else 1
    for ir in range(8):
        for ic in range(8):
            for fr in range(8):
                for fc in range(8):
                    cap = board[fr][fc]
                    end, err = mv(board, (ir,ic,fr,fc), c)
                    if not err:
                        if end:
                            revertMove(board, (ir,ic,fr,fc), cap)
                            return typ*900000, (ir,ic,fr,fc)
                        val, cmove = getVal(level+1, dVal, typ*-1, board)
                        if val*typ > dVal*typ:
                            dVal = val
                            move = (ir,ic,fr,fc)
                        if dVal*typ > parentVal*typ:
                            revertMove(board, (ir,ic,fr,fc), cap)
                            return dVal, (ir,ic,fr,fc)
                        revertMove(board, (ir,ic,fr,fc), cap)
    return dVal, move

def playMove(board, p):
    typ = 1 if p == 1 else -1
    val, move = getVal(0, p*90000, typ ,board)
    return move
