import random
import socket
import threading
import sys
# Set up the socket

IP = 'localhost'
Port = int(sys.argv[1])
addr = ('localhost',Port)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	serversocket.bind(addr)
	print("Starting the server on : ", '127.0.0.1:',Port)
except:
	print("Error while binding to the specified port ")
	exit()
serversocket.listen(5)
try:
	print("Waiting for a connection")
except KeyboardInterrupt:
	print('Interrupted')
	exit()
# Function definitions

def handleclient(port, clientaddress):
	global available1, available2
	addr = ('localhost', port)
	s_conne = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s_conne.bind(('localhost', port))
	except:
		print("Error while binding to the specified port ")
		exit()
	s_conne.listen(5)
	serversocket, c_addr = s_conne.accept()
	notfound = True
	# Receive the client's greeting
	clientgreeting = serversocket.recv(1024)
	# Send the welcome message to the client
	welcomemessage = "Welcome to the number guessing game!\nEnter the range"
	serversocket.send(welcomemessage.encode('ascii'))
	clientgreeting = serversocket.recv(1024)
	xy=clientgreeting.decode('ascii').split(" ")
	x,y=int(xy[0]),int(xy[1])
	numberofguesses = 0
	# Generate a random number for the client to try and guess
	numbertoguess = generatenumber(x,y)
	# Main loop
	while numberofguesses<5:
		messagetosend = ("you have " + str(5 - numberofguesses) + " attemps")
		serversocket.send(messagetosend.encode('ascii'))
		guess = serversocket.recv(1024)
		guessstring = guess.decode('ascii')
		#print(guessstring)
		# Split the guess string up to get the integer guessed
		guess = int(guessstring)
		# Incremenent the counter of the number of guesses
		numberofguesses += 1
		running = 1
		# If the player has guessed correctly
		if (guess == numbertoguess):
			messagetosend = ("You win!")
			serversocket.send(messagetosend.encode('ascii'))
			notfound=False
			break
		else:
			if numberofguesses == 5:
				messagetosend = ("You lose")
				serversocket.send(messagetosend.encode('ascii'))
				break
			# Calculate how far the player was away from the actual number
			difference = guess - numbertoguess
			if difference < 0:
				messagetosend = ("Greater")
			else:
				messagetosend = ("Less")
			# Send the response to the player
			serversocket.send(messagetosend.encode('ascii'))
	# Close the connection	
	serversocket.close()
	if port == Port1:
		available1 = True
	else:
		available2 = True

def generatenumber(x,y):
	return random.randrange(x, y)

# Main server loop
serversocket.settimeout(2)
available1=True
Port1=1234
Port2=1235

try:
	while True:
		try:
			clientsocket, clientaddress = serversocket.accept()
			# Check if the server is full
			if threading.active_count() < 3:
				print('Client connected')
				print("Waiting for a connection")
			else:
				print('The server is full')
				print("Waiting for a connection")
				clientsocket.sendall('The server is full'.encode('ascii'))
				clientsocket.close()
				continue
			if available1==True:
				available1 = False
				c_addr=('localhost',Port)
				clientsocket.sendall(str(Port1).encode('ascii'))
				t = threading.Thread(target=handleclient, args=(Port1, c_addr))
				t.start()
			else:
				# Assign the second port for the client and create a thread
				available2 = False
				c_addr = ('localhost', Port2)
				clientsocket.sendall(str(Port2).encode('ascii'))
				t = threading.Thread(target=handleclient, args=(Port2, c_addr))
				t.start()
		except socket.timeout:
			Print = False
			continue
		except Exception as e:
			print(e)
			break
except KeyboardInterrupt:
	print('Shutting down the server...')
	# start the thread


