# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Megan Volpano
#   Date:   11/10/14
#   File:   UDPPingerServer.py
# - - - - - - - - - - - - - - - - - - - - - -

# Code from Jim Kurose's Socket Programming Assignment 2: UDP Pinger

import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('10.11.116.212', 12000)) #IP address of client

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
