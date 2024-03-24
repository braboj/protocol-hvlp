"""
What is a socket?
A socket is an endpoint for sending and receiving data across a network. It is the fundamental building block of
network communications. It is a way of connecting two nodes on a network to communicate with each other. The socket
contains the address, the port number and the protocol that will be used to communicate with the other node.

What is a server socket?
A server socket is a socket that waits for incoming connections. When a client connects to the server socket, the
server creates a new socket to communicate with the client. When the accept method is called on the server socket, it
blocks the execution of the program until a client connects to the server socket using the 3-way handshake.

What is a client socket?
A client socket is a socket that connects to a server socket. Once the connection is established, the client and server
can communicate with each other using the new socket.

"""

import socket

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the address and port
server_socket.bind(('127.0.0.1', 12345))

# Listen for incoming connections
server_socket.listen(1)

while True:

    # The accept method returns a new socket and the address of the client that
    # connected to the server socket
    connection, address = server_socket.accept()

    # Reiceive the data using the new socket
    data = connection.recv(1024)

    # Send the data back to the client
    connection.send(data)

    # Close the connection
    connection.close()
