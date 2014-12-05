# - - - - - - - - - - - - - - - - - - - - - -
#   Author: Megan Volpano
#   Date:   11/23/14
#   File:   SMTPClient.py
# - - - - - - - - - - - - - - - - - - - - - -

from socket import *
import ssl
import base64

# Input your gmail credentials for: 
username = ''
password = ''
sender = "<>"

# Input the recipient's email address for:
recipient = "<>"


msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 465)

# Create socket called clientSocket and establish a TCP connection with mailserver
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
ssl_clientSocket = ssl.wrap_socket(clientSocket)
ssl_clientSocket.connect((mailserver))
# Fill in end

recv = ssl_clientSocket.read(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response.
print "HELO Alice"
heloCommand = 'HELO Alice\r\n'
ssl_clientSocket.write(heloCommand)
recv1 = ssl_clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'

# Gmail requires you to authenticate
print "AUTH LOGIN"
print "Username:" # used to format printed output
authCommand = 'AUTH LOGIN\r\n'
ssl_clientSocket.write(authCommand)
recv3 = ssl_clientSocket.read(1024)
print recv3
if recv3[:3] != '334':
    print '334 reply not received from server.'
    
# Send username and print server response.
# The Gmail server only accepts authentication credentials in base64
print "Password:" # used to format printed output
userName = base64.b64encode(username) + '\r\n'
ssl_clientSocket.write(userName)
username_recv = ssl_clientSocket.read(1024)
print username_recv
if username_recv[:3] != '334':
    print '334 reply not received from server'

# Send password and print server response.
passWord = base64.b64encode(password) + '\r\n'
ssl_clientSocket.write(passWord)
password_recv = ssl_clientSocket.read(1024)
print password_recv
if password_recv[:3] != '235':
    print '235 reply not received from server'

# Send MAIL FROM command and print server response.
# Fill in start
mailFromCommand = 'MAIL FROM: ' + sender + '\r\n'
print mailFromCommand
ssl_clientSocket.write(mailFromCommand)
recv4 = ssl_clientSocket.read(1024)
print recv4
if recv4[:3] != '250':
    print '250 reply not received from server'
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
rcptToCommand = 'RCPT TO: ' + recipient + '\r\n'
print rcptToCommand
ssl_clientSocket.write(rcptToCommand)
recv5 = ssl_clientSocket.read(1024)
print recv5
if recv5[:3] != '250':
    print '250 reply not received from server'
# Fill in end

# Send DATA command and print server response.
# Fill in start
dataCommand = 'DATA\r\n'
ssl_clientSocket.write(dataCommand)
recv6 = ssl_clientSocket.read(1024)
print recv6
if recv6[:3] != '354':
    print '354 Enter mail, end with "." on a line by itself'
# Fill in end

print "DATA"

# Send message data.
# Fill in start
ssl_clientSocket.write(msg)
print 'Message is: ', msg
# Fill in end

# Message ends with a single period.
# Fill in start
ssl_clientSocket.write(endmsg)
print 'End message (to let the server know your message is complete) is: ', endmsg
# Fill in end

recv7 = ssl_clientSocket.read(1024)
print recv7
if recv7[:3] != '250':
    print '250 reply not received from server'

# Send QUIT command and get server response.
# Fill in start
print "QUIT"
quitCommand = 'QUIT\r\n'
ssl_clientSocket.write(quitCommand)
recv8 = ssl_clientSocket.read(1024)
print recv8
if recv8[:3] != '221':
    print '221 reply not received from server'
    pass
# Fill in end
