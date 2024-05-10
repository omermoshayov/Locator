"""
    omer moshayov
    Locator Client
"""

import socket
import threading
from constants import*
import sys
from get_loc import *
import winsound


class Client(object):
    """
        a user
    """
    def __init__(self, ip, port, name):
        self.name = name
        self.thread_counter = RESET
        try:
            self.user_socket = Client.initiate_client_socket(ip, port)

        except socket.error as msg:
            print('Connection failure: %s\n terminating program' % msg)
            sys.exit(SYS_EXIT)

    def activate_thread(self, ip, port):
        """
        starting thread
        """
        thread = threading.Thread(target=self.thread_function, args=(ip, port))
        thread.start()

    def thread_function(self, ip, port):
        """
        creates the receiving socket that gets the messages.
        client stays on listen
        """
        receiver_socket = Client.initiate_client_socket(ip, port)
        self.send_receiving_to_server(receiver_socket)
        done = False
        while not done:
            try:
                msg = self.receive_msg(receiver_socket)
                request = msg.split()
                req = request[FIRST]
                print(msg)
                print(request)
                if req == "GET_LOCATION":
                    response = self.get_location()
                    self.send_request_to_server(response, receiver_socket)
                elif req == "ADD":
                    self.send_request_to_server(msg, receiver_socket)
                elif req == "BEEP":
                    response = self.beep()
                    self.send_request_to_server(response, receiver_socket)
            except socket.error as e:
                print("thread_function: ", e)

    def get_location(self):
        """
        returns the location as a string which
        contains the latitude and the longitude.
        uses the get_lat_lon action from the
        Location_handler class
        """
        location = Location_handler.get_lat_lon()
        return location

    def beep(self):
        """
        makes a sound
        """
        for x in range(BEEP_TIMES):
            winsound.Beep(BEEP_VOLUME, BEEP_LENGTH)
        return "Beeped"

    @staticmethod
    def initiate_client_socket(ip, port):
        """
        creates the client socket using the ip and port
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            return client_socket
        except socket.error as msg:
            print("socket error: ", msg)

    def send_command(self, request):
        """
        sends the command to the server by usuing
        the send_request_to_server method.
        """
        rsp = ""
        request = request.rstrip()
        if self.valid_request(request):
            self.send_request_to_server(request, self.user_socket)
        return rsp

    def handle_user_input(self):
        """
        handles the input of the user.
        """
        try:
            request = ""
            while request.upper() != 'EXIT':
                request = input('please enter request ')
                if self.valid_request(request):
                    self.send_request_to_server(request, self.user_socket)
                    self.handle_server_response()
                else:
                    if request.upper() != "EXIT":
                        print("illegal request")
        except socket.error as e:
            print("handle_user_input- socket error:", e)
        except Exception as e:
            print("handle_user_input- general error:", e)

    @staticmethod
    def valid_request(request):
        """
        The action verifies that we have received a valid request.
        :param request: the request from the server
        :return: True if valid, else...
        """
        req_and_prms = request.split()
        if req_and_prms[FIRST] == "EXIT":
            return True
        elif req_and_prms[FIRST].upper() == 'GET_LOCATION' and \
                (req_and_prms[SECOND] and req_and_prms[THIRD]).isalpha():
            return True
        elif req_and_prms[FIRST].upper() == "SEARCH" and \
                (req_and_prms[SECOND] and req_and_prms[THIRD]).isalpha():
            return True
        elif req_and_prms[FIRST].upper() == "BEEP" \
                and (req_and_prms[SECOND] and req_and_prms[THIRD]).isalpha():
            return True
        elif req_and_prms[FIRST].upper() == "ADD" \
                and (req_and_prms[SECOND] and req_and_prms[THIRD]).isalpha():
            return True
        return False

    def send_request_to_server(self, request, sock):
        """
        Sends the request to the server
        :param request: server's request
        :param sock: the socket that needs
        to be used to send the request
        """
        encoded_msg = request.encode()
        l = len(encoded_msg)
        ll = str(l)
        lll = ll.zfill(SIZE_LEN)
        llll = lll.encode()
        sock.send(llll + request.encode())

    def handle_server_response(self):
        """
        An action that receives and prints the server's response
        """
        data = Client.receive_msg(self.user_socket)
        return data

    def send_receiving_to_server(self, receiver_socket):
        """
        send the name of the client to the server
        for adding it to the dictionary
        """
        msg = "Receiving " + self.name
        encoded_msg = msg.encode()
        l = len(encoded_msg)
        ll = str(l)
        lll = ll.zfill(SIZE_LEN)
        llll = lll.encode()
        receiver_socket.send(llll + msg.encode())

    @staticmethod
    def receive_msg(server_socket):
        """
            An action that reads the message from the socket using
            the recv command.
        """
        row_msg = Client.my_recv(server_socket)
        return row_msg.decode()

    @staticmethod
    def my_recv(sock):
        """
        receiving the request from the server in small parts.
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

    def send_and_receive(self, request):
        """
        handles the messages the are being
        sent from the GUI.
        sends the messages to the client and
        wait for the response. then sends the
        response for the GUI.
        :param request: command and params
        :return: the response from the server
        """""
        data = ''
        if self.valid_request(request):
            self.send_request_to_server(request, self.user_socket)
            data = self.handle_server_response()
        return data

    def set_name(self, name):
        """
        gets a name and sets the clients
        name to the given name.
        """
        self.name = name


def main():
    """ constructs a client and runs it """
    f = open("client_sign_up.txt", 'r')
    contents = f.read()
    lst = contents.split()
    nm = lst[FIRST] + " " + lst[SECOND]
    client = Client(CLIENT_IP, PORT, nm)
    client.thread_function(CLIENT_IP, PORT)


if __name__ == "__main__":
    main()
