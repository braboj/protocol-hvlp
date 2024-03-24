"""
What is a socket?

The socket is a wrapper that provides access to the underlying operating system's network communication capabilities.
Depending on the parameters passed to the socket constructor, the socket can be used to communicate using different
protocols and different types of communication. It unifies and simplifies the process of sending and receiving data
across a network regardless of the underlying protocol stack and operating system.

Typically, the socket API contains the following methods:

- socket(): creates a new socket object
- bind(): binds the socket to an address and port number on the local machine
- listen(): listens for incoming connections on the server socket
- accept(): accepts an incoming connection and returns a new socket and the address of the client
- connect(): connects to a server socket
- send(): sends data to the other node
- recv(): receives data from the other node
- close(): closes the connection and the socket


What is a client socket?
A client socket is a socket that connects to a server socket. Once the connection is established, the client and server
can communicate with each other using the new socket.

A client socket uses the following methods:

- connect(): connects to a server socket
- send(): sends data to the server
- recv(): receives data from the server
- close(): closes the connection and the socket


What is a server socket?
A server socket is a socket that waits for incoming connections. When a client connects to the server socket, the
server creates a new socket to communicate with the client. When the accept method is called on the server socket, it
blocks the execution of the program until a client connects to the server socket using the 3-way handshake.

A server socket uses the following methods:

- bind(): binds the server socket to an address and port number on the local machine
- listen(): listens for incoming connections on the server socket
- accept(): accepts an incoming connection and returns a new socket and the address of the client


What is a connection socket?

A connection socket is a socket that is created when a client connects to a server socket. The connection socket is used
to communicate with the client. The connection socket is created by the server socket when the accept method is called.

A connection socket uses the following methods:

- send(): sends data to the other node
- recv(): receives data from the other node
- close(): closes the connection and the socket

"""

import socket

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('127.0.0.1', 12345))

# Send the data
client_socket.send(b'Hello, World!')

# Receive the data
data = client_socket.recv(1024)

# Print the received data
print(data)

# Close the connection
client_socket.close()
