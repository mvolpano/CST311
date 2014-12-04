# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Megan Volpano & Sydney Nguyen
#   Date:   11/10/14
#   File:   UDPPingerClient.py
# - - - - - - - - - - - - - - - - - - - - - -

from socket import *
import time

# Skeleton code from Jim Kurose's Socket Programming Assignment 2: UDP Pinger

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
#-socket.AF_INET is a constant, which says that our socket will connect
#  using an IPv4 address
client_socket = socket(AF_INET, SOCK_DGRAM)

#sets the timeout at 1 second
client_socket.settimeout(1)
#keeping track of sequence number
sequence_number = 1
dest = '10.11.116.212' # IP address of the server to which you are sending the packet
port = 12000
print("Pinging " + dest + " on port " + str(port))
while sequence_number <= 10:
    #This is the message that will be sent to the server socket
    data = "Ping"
    #assigns the current time to a variable
    start = time.time() 
    #Sending the message through the socket. It needs to be encoded into bytes
     # because python's string object is not a string of bytes by default
    client_socket.sendto(data,(dest, port)) #IP address of server

    try:
        buffer = client_socket.recv(1024).decode('utf-8')
        #calculates how much time has elapsed since the start time
        elapsed = (time.time() - start)
        print("sequence #" + str(sequence_number) + "  RTT: " + str(round(elapsed*1000,3)) + "ms")
        sequence_number += 1
    #if the socket takes longer that 1 second
    except timeout:
        print("sequence #" + str(sequence_number) + " Request timed out")
        sequence_number += 1
        if sequence_number > 10:
            #closes the socket after 10 packets
            client_socket.close()
                  
