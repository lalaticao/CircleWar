from socket import *

s=socket()
#s.connect(("192.168.1.109",10800))
while True:
    print "Enter a valid ip address to connect and chat."
    addr=raw_input()
    #s.connect((addr,10800))
    try:
        s.connect((addr,10800))
        break
    except Exception(e):
        print "Connection Error:",e
print "Connection is built. Now have fun! (Enter # to quit)"
while True:
    print "You:",
    t=raw_input()
    if t=='#':
        break
    
    try:
        s.sendall(t)
    except:
        print "Failed to send...Enter to quit."
        input()
        break
    
    try:
        print "He/She:",s.recv(1024)
    except:
        print "Can no more receive anything...Enter to quit."
        input()
        break
s.close()
