# coding: utf-8
from session import *
import socket
import threading


class Server(object):

    def __init__(self, ip_addr, port, session_type):
        self.ip_addr = ip_addr
        self.port = port
        self.session_type = session_type
        self.srv_sock = socket.socket()
        self.session_pool = []

    def run(self):
        self.srv_sock.bind((self.ip_addr, self.port))
        self.srv_sock.listen(0)

        while True:

            # Wait for new connection requests
            connection, addr_info = self.srv_sock.accept()

            # Start the correspondign session thread
            session = self.session_type(connection, addr_info)
            t = threading.Thread(target=session.run, args=[connection, addr_info])
            t.start()

            # Save the current sessiono in the session pool
            self.session_pool.append(t)


if __name__ == "__main__":
    server = Server(ip_addr='localhost', port=65432, session_type=EchoSession)
    server.run()
