# coding: utf-8
import socket


class Client(object):

    def __init__(self, srv_addr, port):
        self.srv_addr = srv_addr
        self.port = port
        self.sock = socket.socket()

    def run(self):

        # Connect to the server
        self.sock.connect((self.srv_addr, self.port))

        # Wait for user input and send the data
        while True:
            message = input()
            self.sock.send(message)
            if message == 'stop':
                break
            data = self.sock.recv(1024)
            print(data)

        self.sock.close()


if __name__ == "__main__":
    client = Client(srv_addr='localhost', port=65432)
    client.run()
