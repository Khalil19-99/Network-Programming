from socket import *
import sys
print ("Connecting to server...")
IP = sys.argv[1]
Port = int(sys.argv[2])
addr = (IP,Port)
# Set up the socket as an Internet facing streaming socket
clientsocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server on port 
try:
	clientsocket.connect(addr)
except ConnectionRefusedError:
	print ("Server is unavailable1")
	exit(0)
response = clientsocket.recv(1024)
if response.decode('ascii') == 'The server is full':
	print(response.decode('ascii'))
	exit(0)
Port1=int(response.decode('ascii'))


clientsocket.close()
clientsocket = socket(AF_INET, SOCK_STREAM)
try:
	clientsocket.connect((IP,Port1))
except ConnectionRefusedError:
	print ("Server is unavailable2")
	exit(0)
print("connected!")
# Send the greeting message to the server, as specified by the requirements
message = "Hello from client"
clientsocket.send(message.encode('ascii'))
# Wait for a response, then print said response to the console
response = clientsocket.recv(1024)
print(response.decode('ascii'))
message=input("")
clientsocket.send(message.encode('ascii'))
trials=0

while trials<5:
	trials+=1
	guess=0
	# Ask for user to guess a number
	response = clientsocket.recv(1024).decode('ascii')
	print(response)
	guess = input()
	# Format the guess, ready to send to the server
	guessstring =str(guess)
	# Send the guess
	clientsocket.send(guessstring.encode('ascii'))

	# Wait for the response from the server
	response = clientsocket.recv(1024).decode('ascii')
	print (response)

	# Determine if the game is over
	if (response == "You win!"):
		break
	if (response == "You lose"):
		break

clientsocket.close()

