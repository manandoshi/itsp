def checkAttack(board, color, r, c):
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] != 0:
                if board[i][j].color != color and board[i][j].validMove(board, i, j, r, c):
                    return True
    return False

def checkValidity(board, color, ir, ic, fr, fc):
    b2=[]
    for i in board:
        b2.append(i[:])
    
    b2[fr][fc] = b2[ir][ic]
    b2[ir][ic] = 0
    
    
    return not checkCheck(b2, color)

def checkCheck(board, color):
     
    kr=8
    kc=8
    
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] != 0:
                if board[i][j].name == "K" and board[i][j].color == color:
                    kr = i
                    kc = j
                    break
        if not (kr == 8 and kc == 8):
            break
    
    if not checkAttack(board, color, kr, kc):
        return False
    return True


def checkMate(board, color):
    for ir in range(0,8):
        for ic in range(0,8):
            if board[ir][ic] != 0:
                    if board[ir][ic].color == color:
                        for fr in range(0,8):
                            for fc in range(0,8):
                                if board[ir][ic].validMove(board, ir, ic, fr, fc):
                                    if checkValidity(board, color, ir, ic, fr, fc):
                                        return False
    if not checkCheck(board, color):
        return "Stale"
    else:
        print "MATE \n"
        return "Mate"
class rook:
    def __init__(self,color):
        self.color = color
        self.name="R"
        self.hasMoved = False
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        
        if ir==fr:
            for i in range(min(ic,fc)+1,max(ic,fc)):
                if board[ir][i] != 0 :
                    return False
            if board[ir][fc] != 0:
                if board[ir][fc].color == self.color:
                    return False
            return True
        
        if ic==fc:
            for i in range(min(ir,fr)+1,max(ir,fr)):
                if board[i][ic] != 0 :
                    return False
            if board[fr][fc] != 0:
                if board[fr][fc].color == self.color:
                    return False
                return True
            return True
        return False

class knight:
    def __init__(self, color):
        self.color = color
        self.name = "N"
        self.hasMoved=False
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        if abs((ir-fr)*(ic-fc)) == 2:
            if board[fr][fc] != 0:
                if board[fr][fc].color == self.color:
                    return False
                return True
            return True
        return False

class bishop:
    def __init__(self, color):
        self.color = color
        self.name = "B"
        self.hasMoved=False
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        if abs(ir-fr) == abs(ic-fc):
            for i in range(1,abs(fr-ir)):
                s = lambda x : x/abs(x)
                if board[ir + s(fr-ir)*i][ic + s(fc-ic)*i] != 0:
                    return False
            if board[fr][fc] != 0:
                if board[fr][fc].color == self.color:
                    return False
                return True
            return True
        return False

class king:
    def __init__(self, color):
        self.color = color
        self.name = "K"
        self.hasMoved = False
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        if abs(ir-fr) | abs(ic-fc) == 1:
            if board[fr][fc] != 0:
                if board[fr][fc].color == self.color:
                    return False
                return True
            return True
        elif (not self.hasMoved) and fr == ir:
            for i in range(min(ic,fc)+1,max(ic,fc)+1):
                if board[ir][i] != 0 :
                    return False
            if fc == 6:
                if board[ir][7] != 0:
                    if board[ir][7].name != "R":
                       return False
                    if board[ir][7].hasMoved:
                        return False
                    if checkAttack( board, self.color, ir, 6) or checkAttack( board, self.color, ir, 5) or checkAttack( board, self.color, ir, 4):
                        return False
                    return True
                return False
            if fc == 2:
                if board[ir][1] != 0:
                    return False
                if board[ir][0] != 0:
                    if board[ir][0].name != "R":
                        return False
                    if board[ir][0].hasMoved:
                        return False
                    if checkAttack( board, self.color, ir, 2) or checkAttack( board, self.color, ir, 3) or checkAttack( board, self.color, ir, i4):
                        return False
                    return True
                return False
            return False
        return False

class pawn:
    def __init__(self, color):
        self.color = color
        self.hasMoved = False
        self.name = "P"
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        if self.color == 1:
            p = -1
        else:
            p = 1
        if (fr-ir)*p <= 0 or abs(fc-ic)>1:
            return False
        if not self.hasMoved:
            if (fr-ir)*p == 2 and ic==fc:
                for i in range(0,2):
                    if board[ir+i*p+p][ic] != 0:
                        return False
                return True

        if (fr-ir)*p == 1:
            if fc==ic and board[fr][fc] == 0:
                return True
            else:
                if board[fr][fc] != 0:
                    if board[fr][fc].color == self.color:
                        return False
                    return True
                return False
            return False
        return False
class queen:
    def __init__(self, color):
        self.color = color
        self.name = "Q"
        self.hasMoved=False
    def __str__(self):
        return ("W" if self.color == 0 else "B") + self.name 
    def validMove(self, board, ir, ic, fr, fc):
        qr = rook(self.color)
        qb = bishop(self.color)
        if (qb.validMove(board, ir, ic, fr, fc) or qr.validMove(board, ir, ic, fr, fc)):
            return True
        else:
            return False

def mv(board, l, c):
    if not ( l[0] >= 0 and l[0] < 8 and l[2] >= 0 and l[2] < 8 and l[1]>=0 and l[1] < 8 and l[3] >= 0 and l[3] < 8) :
        return 0, 1
    if board[l[0]][l[1]] == 0:
        return 0, 2
    if board[l[0]][l[1]].color != c:
        return 0, 3
    if not board[l[0]][l[1]].validMove(board, l[0], l[1], l[2], l[3]):
        return 0, 4
    if not checkValidity(board, c, l[0], l[1], l[2], l[3]):
        return 0, 5
    
    board[l[2]][l[3]], board[l[0]][l[1]] = board [l[0]][l[1]], 0
    board[l[2]][l[3]].hasMoved = True

    if board[l[2]][l[3]].name == "K":
        if abs(l[1]-l[3])==2:
            if l[3]==6:
                board[l[0]][5], board[l[0]][7] = board[l[0]][7], 0
                board[l[0]][5].hasMoved=True
            if l[3]==2:
                board[l[0]][3], board[l[0]][0] = board[l[0]][0] , 0
                board[l[0]][3].hasMoved = True
    end = checkMate(board, 1-c)
    if end:
        print end
        if end == "Mate":
            return c+1, 0
        elif end == "Stale":
            return 3, 0
    return 0, 0
def prnt(board):
    for i in range(0,8):
        for j in range(0,8):
            print board[i][j],
            print '\t',
        print "\n"
def inp():
    ir = input('ir: ')
    ic = input('ic: ')
    fr = input('fr: ')
    fc = input('fc: ')

    return [ir, ic, fr, fc]

def initBoard():
        board = [[ rook(0), knight(0), bishop(0), queen(0), king(0), bishop(0), knight(0), rook(0)],
                [ pawn(0), pawn(0)  , pawn(0)  , pawn(0) , pawn(0), pawn(0)  , pawn(0)  , pawn(0)],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ pawn(1), pawn(1)  , pawn(1)  , pawn(1) , pawn(1), pawn(1)  , pawn(1)  , pawn(1)],
                [ rook(1), knight(1), bishop(1), queen(1), king(1), bishop(1), knight(1), rook(1)]]
        return board

def main():
    end = False
    c = 0
    board = [[ rook(0), knight(0), bishop(0), queen(0), king(0), bishop(0), knight(0), rook(0)],
             [ pawn(0), pawn(0)  , pawn(0)  , pawn(0) , pawn(0), pawn(0)  , pawn(0)  , pawn(0)],
             [ 0, 0, 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0, 0, 0],
             [ pawn(1), pawn(1)  , pawn(1)  , pawn(1) , pawn(1), pawn(1)  , pawn(1)  , pawn(1)],
             [ rook(1), knight(1), bishop(1), queen(1), king(1), bishop(1), knight(1), rook(1)]]
    prnt(board)
    while( not end):
        end, err = mv(board, inp(), c)
        if not err:
            c = 1 - c
            prnt(board)
        else:
            print err

    return

if __name__ == '__main__':
    main()
