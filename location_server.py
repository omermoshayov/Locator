"""
    Omer Moshayov
    Locator Server
"""

import socket
import threading
import sys
from constants import *


class Server(object):
    """
        Find PC server
    """

    def __init__(self, ip, port):
        self.clients = {}
        self.clients_password = {}
        self.clients_lock = threading.Lock()
        self.thread_counter = RESET
        self.server_socket = None
        self.lock = threading.Lock()
        try:
            self.server_socket = Server.initiate_server_socket(ip, port)
        except socket.error as msg:
            print("Connection failure: %s\n terminating program" % msg)
            sys.exit(SYS_EXIT)

    @staticmethod
    def initiate_server_socket(ip, port):
        """
        creates the server socket by using the given ip
        and port.
        starts listening.
        """
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip, port))
            server_socket.listen(LISTEN)
            return server_socket
        except Exception as msg:
            print("General error 1: ", msg)

    def handle_clients(self):
        """
        An action that receives the server socket
        and waits for clients by using the accept operation –
        as soon as service request is received from a customer
        handle_single_client (operation) is called.
        the operation handles the customer until they ask to
        exit or disconnect.
        Then we'll be back waiting for another service request.
        """
        done = False
        while not done:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_single_client, args=(client_socket,))
                client_thread.start()
            except socket.error as msg:
                print("Socket Error: ", msg)
            except Exception as msg:
                print("General error 2: ", msg)

    def handle_single_client(self, client_socket):
        """
        The operation handles the customer until they ask to
        exit or disconnect.
        :return: True if the client sent 'EXIT'
        """
        self.thread_counter += ANOTHER_ONE
        num = self.thread_counter
        print("starting thread", num)
        done = False
        try:
            while not done:
                request, params = Server.receive_client_request(client_socket)
                valid, clients_name = Server.check_client_request(request, params)
                if request is None:
                    break
                print("1 ", request)
                print("2 ", params)
                if valid:
                    response_to_receiver = self.handle_client_request(request, params, client_socket, clients_name)
                    if response_to_receiver == "RECEIVING":
                        done = True
                    else:
                        Server.send(response_to_receiver, client_socket)
        except socket.error as msg:
            print("socket error:", msg)
        except Exception as msg:
            print("general error 2: ", msg)

    @staticmethod
    def receive_client_request(client_socket):
        """
        An action that reads the commands from the socket using
        the recv command.
        :return: the request as a string
        """
        # reads from socket
        raw_request = Server.my_recv(client_socket)
        request = raw_request.decode()
        print("3 ", request)
        # split to request and parameters
        req_and_prms = request.split()
        if len(req_and_prms) > LEN_ONE:
            return req_and_prms[FIRST].upper(), req_and_prms[SECOND:]
        else:
            return req_and_prms[FIRST].upper(), None  # no parameters

    @staticmethod
    def receive_client_response(client_socket):
        """
        An action that reads the response from the
        client's socket using the recv command
        and prints it.
        """
        raw_response = Server.my_recv(client_socket)
        response = raw_response.decode()
        print("4 ", response)
        return response

    @staticmethod
    def my_recv(sock):
        """
        receiving the request from the client in small parts.
        :param sock: receiving socket
        """
        data = b''
        s = sock.recv(SIZE_LEN)
        if s.isdigit():
            size = int(s)
            while size > RESET:
                d = sock.recv(size)
                size -= len(d)
                data += d
        return data

    @staticmethod
    def check_client_request(request, params):
        """
        The action verifies that we have received a valid request.
        :return: True if valid, else...
        """
        name = None
        if params is not None:
            name = params[FIRST] + " " + params[SECOND]
        if request == 'GET_LOCATION' and (params[FIRST] and params[SECOND]).isalpha:
            return True, name
        if request == "RECEIVING" and (params[FIRST] + params[SECOND]).isalpha():
            return True, name
        if request == "EXIT" and params is None:
            return True, None
        if request == "SEARCH" and (params[FIRST] + params[SECOND]).isalpha():
            return True, name
        if request == "BEEP" and (params[FIRST] + params[SECOND]).isalpha():
            return True, None
        if request == "ADD" and (params[FIRST] + params[SECOND]).isalpha():
            return True, None
        return False, None

    def handle_client_request(self, request, params, client_socket, clients_name):
        """
        Gets the request, params and the client_socket and
        sends it to the other client
        """
        if request == "GET_LOCATION":
            return self.send_location(clients_name)
        if request == "RECEIVING":
            self.add_to_dictionary(client_socket, clients_name)
            return "RECEIVING"
        if request == "EXIT":
            return "EXIT"
        if request == "SEARCH":
            response = self.search_in_dictionary(clients_name, params)
            return response
        if request == "BEEP":
            response = self.beep(params)
            return response
        if request == "ADD":
            response = self.add(params, client_socket)
            return response

    def send_location(self, name):
        """
        sending the request get_location
        and the name of the client to the wanted client
        """

        print("5 ", name)
        print("6 ", self.clients)
        if name.upper() in self.clients:
            sock = self.clients[name.upper()]
            Server.send("GET_LOCATION " + name, sock)
            rsp = Server.receive_client_response(sock)
            return rsp
        else:
            return "Client doesn't exist ", None

    def beep(self, params):
        """
        sending the request beep and the name of
        the client to the wanted client
        """
        name = params[FIRST] + " " + params[SECOND]
        if name.upper() in self.clients:
            sock = self.clients[name.upper()]
            Server.send("BEEP " + name, sock)
            rsp = Server.receive_client_response(sock)
            # rsp = "hey"
            return rsp
        else:
            return "not able to beep"

    def add(self, params, client_socket):
        """
        adds the user name and the password of the
        client who signed up to the dictionary of the passwords.
        """
        if len(params) == 3:
            nm = params[FIRST] + " " + params[SECOND]
            pswd = params[THIRD]
            if not self.check_existing_password(pswd):
                return "This password is already taken"
            elif not self.check_existing_username(nm):
                return "This username is already taken"
            else:
                self.clients_password[nm.upper()] = pswd
                self.clients[nm.upper()] = client_socket
                return "Signed up successfully"
    def check_existing_username(self, name):
        """
           Searching if there is already a client with
           the same username.
        """
        flag = False
        for key in self.clients_password:
            if key == name[0]:
                flag = True
        return not flag

    def check_existing_password(self, pswd):
        """
        Searching if there is already a client with
        the same password.
        """
        flag = False
        for key in self.clients_password:
            if self.clients_password[key] == pswd:
                flag = True
        return not flag

    def add_to_dictionary(self, client_socket, clients_name):
        """
        adds the client and the client socket to
        a dictionary
        """
        self.clients[clients_name.upper()] = client_socket
        return None

    def search_in_dictionary(self, client_name, params):
        """
        searching if the client is in the
        dictionary of the client.
        if the client exists, returns True and
        if not returns False.
        """
        nm = client_name
        pswd = params[THIRD]
        if nm.upper() in self.clients_password:
            if self.clients_password[nm.upper()] == pswd:
                return "True"
            return "False"
        return "False"

    @staticmethod
    def send(msg, sock):
        """
        An action that sends the string to the client as binary array
        """
        encoded_msg = msg.encode()
        l = len(encoded_msg)
        ll = str(l)
        lll = ll.zfill(SIZE_LEN)
        llll = lll.encode()
        sock.send(llll + encoded_msg)
def main():
    """ constructs a server and runs it"""
    server = Server(SERVER_IP, PORT)
    server.handle_clients()


if __name__ == "__main__":
    main()
