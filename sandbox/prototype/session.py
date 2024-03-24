# coding: utf-8

class EchoSession(object):

    def __init__(self, client, addr_info):
        self.client = client
        self.addr_info = addr_info

    def run(self):
        print('Connection from {0}'.format(self.client.getpeername()))
        while True:
            data = self.client.recv(1024)
            self.client.send(data)
            print(data, len(data))


class ReverseEchoSession(object):

    def __init__(self, connection, addr_info):
        self.connection = connection
        self.addr_info = addr_info

    @staticmethod
    def run(connection, addr_info):
        print('Connection from {0}'.format(addr_info))
        while True:
            data = connection.recv(1024)
            reverse = data[::-1]
            if data:
                print(data)
            connection.send(reverse)
