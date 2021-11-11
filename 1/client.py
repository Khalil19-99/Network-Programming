# Mohammad Khalil SD-02

import hashlib
import socket
import time
import sys
import os  # Needed for os.path.getsize() to get size of file


time_out=2
serverAddress = "127.0.0.1"
serverPort = 1234
# Delimiter
delimiter = '|';
BUFFER_SIZE = 1024

def send_message(sock, message, timeout, n_trials):
    global serverAddress, serverPort
    for i in range(n_trials):
        try:
            sock.sendto(message, (serverAddress, serverPort))
            sock.settimeout(timeout)
            s_message = sock.recvfrom(BUFFER_SIZE)[0].decode()
            return s_message.split("|")
        except Exception as e:
            print(e)

    return None
def fix(num):
    assert 0 <= num <= 99999
    ret = '0' * 4 + str(num)
    return ret[-5:]

def get_response():
    try:
        rec_msg = UDP_socket.recvfrom(BUFFER_SIZE)[0].decode()
        print ("Server response:")
        return rec_msg
    except:
        return "TIMEOUT"
file_name="innopolis"
serverAddressPort = (serverAddress, serverPort)
f = open("/home/khalil/innopolis.jpg", "rb")
#image = mpimg.imread("/home/khalil/innopolis.jpg")
file_size=os.path.getsize("/home/khalil/innopolis.jpg")
seq=0
UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_socket.settimeout(time_out)  # Set default time-out

print ("\nConnecting to UDP server %s:%s..." % (serverAddress, serverPort))

string = 's' + delimiter + str(seq) + delimiter + "jpg" +delimiter+ str(file_size)
msgFromClient = string
bytesToSend = str.encode(msgFromClient)
UDP_socket.sendto(bytesToSend, (serverAddress, serverPort))
print ("Waiting for server response...")

server_response1 = get_response()
server_response=server_response1.split(delimiter)
if server_response[0] == 'a':
	print("Connection established!")
	seq = int(server_response[1])
	max_size = int(server_response[2])
else:
	print("Connection failed. Try again.")
	exit(0)
header_size = 8
data = f.read(max_size - header_size)
while data:
	# Generating and sending the data message.
	message = ('d' +delimiter+ fix(seq) + delimiter).encode() + data
	s_message_elems = send_message(UDP_socket, message, 0.5, 5)

	if s_message_elems is None:
		print(f"The sever is not responding to the data message with sequence number {seq}! "
			  f"Shutting down...")
		UDP_socket.close()
		exit(0)
	# Checking the correctness of the message received from the server.
	try:
		assert len(s_message_elems) == 2 and s_message_elems[0] == 'a' and int(s_message_elems[1]) == seq + 1
		seq += 1
	except Exception as e:
		print(f"Invalid response to the data message number {cur_seq_n}! Shutting down...")
		UDP_socket.close()
		exit(0)
	data = f.read(max_size - header_size)

# Close socket
print ("Shutting down client.")
UDP_socket.close()

