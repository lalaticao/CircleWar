from socket import *

s=socket()
s.bind(('',10800))
s.listen(1)
print "Wait for a connection..."
client,addr = s.accept()
print "Connection from",str(addr),". (Enter # to quit)"
while True:
    try:
        print "He/She:",client.recv(1024)
    except:
        print "Can no more receive anything...Enter to quit."
        input()
        break
    
    print "You:",
    t=raw_input()
    if t=="#":
        break
    
    try:
        client.sendall(t)
    except:
        print "Failed to send...Enter to quit."
        input()
        break
client.close()
