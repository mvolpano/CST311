# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Megan Volpano
#   Date:   11/10/14
#   File:   UDPPingerClient.py
# - - - - - - - - - - - - - - - - - - - - - -

from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
#-socket.AF_INET is a constant, which says that our socket will connect
#  using an IPv4 address
client_socket = socket(AF_INET, SOCK_DGRAM)
# sets the timeout at 1 second
client_socket.settimeout(1)

seq_num = 1
pings = 10
dest = '10.11.116.212'
port = 12000
print("Pinging " + dest + " on port " + str(port))
while seq_num <= pings:
    # This is the message that will be sent to the server socket
    data = "Hello"
    # current time
    first = time.time() 
    # Sending the message through the socket. It needs to be encoded into bytes
     # because python's string object is not a string of bytes by default
    client_socket.sendto(data,(dest, port)) #IP address of server

    try:
        buffer = client_socket.recv(1024).decode('utf-8')
        #calculates how much time has elapsed since the start time
        rtt = (time.time() - first)
        # printing the sequence number and RTT
        print("sequence #" + str(seq_num) + "  RTT: " + str(round(rtt*1000,3)) + "ms")
        seq_num = seq_num + 1
    #if there is a timeout
    except timeout:
        print("sequence #" + str(seq_num) + "  Request timed out")
        seq_num = seq_num + 1
        
client_socket.close()
