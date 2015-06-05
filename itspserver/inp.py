def inp(p, playerTurn):
    print " Waiting for input from player ", playerTurn
#    print p
    inp = p[playerTurn].recv(1024)
    print "Got input: ", inp
    return inp

def outp(inpt, p, playerTurn):
    print " Sending outp ", inpt, " to player ",playerTurn 
    p[playerTurn].send(inpt)

def outpfeedback(err, playerTurn, p, end):
    if end:
        p[playerTurn].send("End")
        return

    if err:
        print "Sending False to ", playerTurn 
        p[playerTurn].send("False")

    else:
        print "Sending True to ", playerTurn 
        p[playerTurn].send("True")
