# pop3-email-simulator

This program is an implementation of the POP3 email client and server, made as an exercise with Python socket programming in a computer networking course.

# Testing
You can test the program as follows:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python3 server.py <port>` <br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python3 client.py <ip address> <port>` <br/>

If running both the client and server on the same device, localhost can be used as the IP address. 

The server reads all the files in the emails folder. Run the program from the main folder without moving the emails from the emails subfolder. Any additional emails to be added to the server go inside of the emails folder.

# Example

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python3 server.py 5981`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python3 client.py localhost 5981`