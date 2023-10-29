# The client simply sends commands to the server and prints what the server
# responds with.
from socket import * # Socket functionality
import sys           # cmd line arguments

# Check arguments
if len(sys.argv) != 3:
    print("usage: python3 client.py <IP address> <portnumber>")
    sys.exit()

try:
    serverPort = int(sys.argv[2])
    addr = sys.argv[1]
    if addr != "localhost":
        try:
            inet_aton(sys.argv[1])
        except Exception as error:
            print(f"Error: {error}\nusage: python3 client.py <IP address> <portnumber>")
            sys.exit()
    if serverPort < 1024 or serverPort > 65535:
        print("Error: Port number must be larger than 1024 and smaller than 65536")
        print("usage: python3 client.py <IP address> <portnumber>")
        sys.exit()
except Exception as error:
    print(f"Error: {error}\nusage: python3 client.py <IP address> <portnumber>")
    sys.exit()

# Connect to server
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((addr, serverPort))
except Exception as error:
    print(f"Error: {error}")
    sys.exit()

# Client
inp = None
while True:
    # Receive output from the server
    # (The communication starts with the server outputting that it is ready)
    rec = clientSocket.recv(2048)
    print("S: " + rec.decode())

    # If the last input was QUIT, we already printed the server's response
    # Now we close the socket and break the loop
    if inp == "QUIT":
        clientSocket.close()
        break
    
    # Get new input, don't allow empty input
    inp = input("C: ")
    while inp == "":
        inp = input("C: ")

    # Send the command
    clientSocket.send(inp.encode())
