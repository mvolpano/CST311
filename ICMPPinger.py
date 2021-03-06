# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Megan Volpano
#   Date:   11/29/14
#   File:   ICMPPinger.py
# - - - - - - - - - - - - - - - - - - - - - -

# Skeleton code from Jim Kurose's Socket Programming Assignment 5: ICMP Pinger

# MUST RUN AS ROOT FOR CORRECT PERMISSIONS
  # type "sudo su" into terminal before running

from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2

    count = 0
    while count < countTo:
        thisVal = ord(str[count + 1]) * 256 + ord(str[count])
        csum = csum + thisVal
        csum = csum & 0xffffffffL
        count = count + 2

    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffffL

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    # "bbHHh" used for integer formatting
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff  # Convert 16-bit integers from host to network byte order
    else:
        myChecksum = socket.htons(myChecksum)

    print "ICMP request header:", ICMP_ECHO_REQUEST, "   " + str(0), "   " + str(myChecksum), "   " + str(ID), "    " + str(1)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
     # which can be referenced by their position number within the object


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fill in start
        # Fetch the ICMP header from the IP packet
        icmp_header = recPacket[20:28]
        type, code, checksum, packetID, sequence_num = struct.unpack("bbHHh", icmp_header)
  
        print "ICMP reply header:  ", type, "   " + str(code), "   " + str(checksum), "   " + str(packetID), "    " + str(sequence_num)
        if packetID == ID:
            double = struct.calcsize("d") # "d" gives a float
            payload = struct.unpack("d", recPacket[28:28 + double])[0]
            rtt = timeReceived - payload # payload is the time sent in original packet

            return "RTT = " + str(round(rtt, 3)) + " ms\n"
        # Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details 
      # see: http://sock-raw.org/papers/sock_raw

    # Fill in start
    # Create Socket here
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    # Fill in end

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout = 1 means: If one second goes by without a reply from the server,
     # the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print "Pinging " + dest + ":"
    # Sends one ping message to each server listed below
    print "ICMP header fields: Type Code Checksum  ID  Sequence#"
    delay = doOnePing(dest, timeout) 
    print delay
    time.sleep(1) # one second
    return delay


print
print "Africa:  www.google.co.za" 
ping("www.google.co.za")
print "Asia:  www.asiahotel.co.th"
ping("www.asiahotel.co.th")
print "Australia:  www.australia.gov.au"
ping("www.australia.gov.au")
print "Europe:  www.google.co.uk" 
ping("www.google.co.uk")
print "North America:  www.bu.edu"
ping("www.bu.edu")
print "South America:  www.google.com.br"
ping("www.google.com.br")
