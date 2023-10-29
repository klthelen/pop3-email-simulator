from socket import * # Socket functionality
import sys           # cmd line arguments 
import os            # for directory pathing

class EmailList:
    """ Class implementation to store a list of emails. """
    
    class Email:
        """ Class implementation to store information about an email. """
        def __init__(self, file_name, header, body, size):
            self.file_name = file_name.strip()
            self.header = header.strip()
            self.body = body.strip()
            self.size = size

            
        def get_size(self):
            """ Returns the size of the email in bytes. """
            return self.size


        def get_file_name(self):
            """ Returns the file name associated with the email. """
            return self.file_name


        def get_header(self):
            """ Returns the header of the email. """
            return self.header


        def get_body(self, n=True):
            """ Returns the body of the email up to n lines.
            If n is ommitted or explicitly stated to be True, returns the entire body.
            """
            if n is True:
                return self.body
            else:
                split_body = self.body.split("\n")
                body = ""
                if n > len(split_body):
                    n = len(split_body)
                for i in range (0, n):
                    body += split_body[i] + "\n"
                return body.strip()

        
        def get_entire_email(self):
            """ Returns the entire contents of the email. """
            header = self.get_header()
            body = self.get_body()
            return f"{header}\n\n{body.strip()}"


    def __init__(self):
        self.email_list = {}
        self.deleted_email_ids = {}
        self.maildrop = 0
        self.emails = 0

        
    def append(self, email_num, email):
        """ Appends an email to the email list. """
        self.email_list[email_num] = email
        self.emails += 1
        self.maildrop += email.get_size()

        
    def get_maildrop(self):
        """ Returns the sum of the size of all emails in the email list. """
        return self.maildrop

    
    def get_number_of_emails(self):
        """ Returns the number of emails in the email list. """
        return self.emails

    
    def get_listing(self):
        """ Returns the listing of emails in the email list. """
        listing = ""
        for key, email in self.email_list.items():
            listing += "\n"
            listing += f"{key} {email.get_size()}"
        return listing

    
    def get_email(self, email_num):
        """ Returns the entire email associated with the provided email number. """
        try:
            email = self.email_list[email_num]
        except:
            email = None
        return email


    def top(self, email_num, n):
        """ Returns the header and the first n lines of the body of the email. """
        email = self.get_email(email_num)
        if email is None:
            return None
        else:
            if n > 0:
                return f"{email.get_header()}\n\n{email.get_body(n=n)}"
            else:
                return f"{email.get_header().strip()}"
            
    
    def delete_email(self, email_num):
        """ Deletes the entire email associated with the email number from the server.
        Returns True if the email is successfully deleted.
        Returns False if the email has already been deleted.
        Returns None if the email has not existed since the server has loaded emails.
        """
        try:
            email = self.email_list[email_num]
        except:
            try:
                deleted_email = self.deleted_email_ids[email_num]
                if deleted_email == True:
                    return False
            except:
                return None
        file_name = email.get_file_name()
        file_size = email.get_size()
        cwd = os.getcwd()
        directory = "emails"
        path = os.path.join(cwd, directory)
        os.remove(os.path.join(path, file_name))
        del self.email_list[email_num]
        self.deleted_email_ids[email_num] = True
        self.emails -= 1
        self.maildrop -= file_size
        return True 

    
    def load_emails(self):
        """ Reads all emails from the emails folder and loads them into the server. """
        self.email_list = {}
        cwd = os.getcwd()
        directory = "emails"
        path = os.path.join(cwd, directory)
        if os.path.exists(path):
            i = 1
            for email_file in os.listdir(path):
                file_size_in_bytes = os.path.getsize(os.path.join(path, email_file))
                with open(os.path.join(path, email_file), 'r') as f:
                    header = ""
                    body = ""
                    h = True
                    for line in f:
                        if h is True:
                            if line != "\n":
                                header += line
                            else:
                                h = False
                        else:
                            if line != "\n":
                                body += line
                    self.append(i, EmailList.Email(email_file,
                                                   header,
                                                   body,
                                                   file_size_in_bytes))
                    i += 1
        else:
            print("Error: emails directory not found, cannot load emails")
            sys.exit()

            
def check_inputs():
    """ Validates the command line inputs for the server to function.
    If any input is invalid, returns a usage statement and terminates the program.
    """
    if len(sys.argv) != 2:
        print("usage: python3 server.py <portnumber>")
        sys.exit()
        
    try:
        port = int(sys.argv[1])
        if port < 1024 or port > 65535:
            print("Error: Port number must be larger than 1024 and smaller than 65536")
            print("usage: python3 server.py <portnumber>")
            sys.exit()
        return port
    except Exception as error:
        print(f"Error: {error}\nusage: python3 server.py <portnumber>")
        sys.exit()


def handle_message(email_list, args):
    """ Takes the email_list and the split message received from the client.
    Handles the message according to the command provided.
    """
    command = args[0]
    if command == "STAT":
        if len(args) != 1:
            return f"-ERR usage: STAT"
        number_of_emails = email_list.get_number_of_emails()
        size_of_maildrop = email_list.get_maildrop()
        return f"+OK {number_of_emails} {size_of_maildrop}"
    elif command == "LIST":
        if len(args) != 1:
            return f"-ERR usage: LIST"
        email_list.load_emails()
        listing = email_list.get_listing()
        return f"+OK Mailbox scan listing follows {listing}"
    elif command == "RETR":
        if len(args) != 2:
            return f"-ERR usage: RETR <X>"
        email_number_as_string = args[1]
        try:
            email_number = int(email_number_as_string)
            email = email_list.get_email(email_number)
            if email is not None:
                return f"+OK {email.get_size()} octets\n{email.get_entire_email()}"
            else:
                return f"-ERR no such message"
        except:
            return f"-ERR no such message"
    elif command == "DELE":
        if len(args) != 2:
            return f"-ERR usage: DELE <X>"
        email_number_as_string = args[1]
        try:
            email_number = int(email_number_as_string)
            response = email_list.delete_email(email_number)
            if response == True:
                return f"+OK message deleted"
            elif response == False:
                return f"-ERR message {email_number} already deleted"
            else:
                return f"-ERR no such message"
        except:
            return f"-ERR no such message"
    elif command == "TOP":
        if len(args) != 3:
            return f"-ERR usage: TOP <X> <n>"
        email_number_as_string = args[1]
        n_as_string = args[2]
        try:
            email_number = int(email_number_as_string)
        except:
            return f"-ERR no such message"
        try:
            n = int(n_as_string)
            if n < 0:
                return f"-ERR invalid line number"
        except:
            return f"-ERR invalid line number"
        response = email_list.top(email_number, n)
        if response is not None:
            return f"+OK top of message follows\n{response}"
        else:
            return "-ERR no such message"
    else:
        return "-ERR invalid command"


def main():
    """ The main server function.
    Runs the POP3 server indefinitely.
    """
    email_list = EmailList()
    email_list.load_emails()

    port = check_inputs()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(1)
    while True:
        print("+OK POP3 server is ready to receive connections")
        conn, addr = server_socket.accept()
        conn.send("+OK POP3 server ready".encode())
        print(f"+OK Connection from {addr}")
        while True:
            message = conn.recv(2048).decode()
            if not message:
                break
            args = message.split()
            if args[0] == "QUIT":
                conn.send("+OK POP3 server signing off".encode())
                print(f"+OK Connection with {addr} closed")
                conn.close()
                break
            output = handle_message(email_list, args)
            conn.send(output.encode())
main()
