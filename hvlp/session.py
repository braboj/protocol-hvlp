# encoding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from hvlp.packets import *
from hvlp.defines import *

from abc import ABCMeta, abstractmethod
from six import with_metaclass

import threading
import socket
import logging


class Session(with_metaclass(ABCMeta)):
    """ Template class for all session's types """

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def run(self):
        raise NotImplementedError


class EchoSession(Session):
    """ Demo session that will return back any message sent by the client """

    def __init__(self, client, *args, **kwargs):
        self.client = client
        super(EchoSession, self).__init__(client, *args, **kwargs)

    def run(self):
        print('Connection from {0}'.format(self.client.getpeername()))
        while True:
            try:
                data = self.client.recv(1024)
                self.client.sendall(data)

            except socket.error:
                pass


class HvlpSession(Session):
    """ Hilscher Variable Protocol Length Session Class

    The session is a thread that works with a specific protocol version and handles the incoming
    packets from the client. The session is also responsible to forward incoming publish packets
    to all the subscribers of the topic in the publish packet.

    Args:
          client        : Client connection
          register      : Register instance that created the broker

    Attributes:
        self.client     : Client connection
        self.register   : Reference to the broker register
        self.state      : Session state
        self.terminate  : Stop signal for all threads in the session
        self.log        : Logger instance
        self.lock       : Lock instance for shared resources
        self.stream_in  : Input byte stream

    """

    WAIT_CONNECT = 0
    CONNECTED = 1
    ERROR_NO_DATA = 10035

    def __init__(self, client, register, *args, **kwargs):

        # Logging configuration
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(logging.NullHandler())

        # Connection attributes
        self.client = client

        # Session management
        self.register = register
        self.state = self.WAIT_CONNECT
        self.terminate = threading.Event()

        # Shared resources
        self.lock = threading.Lock()
        self.stream_in = b""

        # Call the parent constructor
        super(HvlpSession, self).__init__(client, register, *args, **kwargs)

    ###############################################################################################

    def on_packet(self, packet):
        """ Packet handler that might be overriden by a custom session implementation

        Args:
            packet  : A packet object

        """

        self.log.debug("{0} from {1}".format(packet, self.client.getpeername()))

        # Handle subscribe packets
        if packet.id == SubscribePacket.ID:
            self.on_subscribe(packet.topics)

        # Handle unsubscribe packets
        elif packet.id == UnsubscribePacket.ID:
            self.on_unsubscribe(packet.topics)

        # Handle publish packets
        elif packet.id == PublishPacket.ID:
            self.on_publish(packet)

        # Handle unknown packets
        else:
            self.log.debug("UNEXPECTED PACKET: {0}".format(packet))

    ###############################################################################################

    def on_subscribe(self, topics):
        """ Subscribe the client on subscribe request

        Args:
            topics  : List of topic names

        """

        self.register.append(topics=topics, client=self.client)
        self.log.debug(self.register)

    ###############################################################################################

    def on_unsubscribe(self, topics):
        """ Unsubscribe the client on subscribe request

        Args:
            topics  : List of topic names

        """

        self.register.remove(topics=topics, client=self.client)
        self.log.debug(self.register)

    ###############################################################################################

    def on_publish(self, packet):
        """ Forward publosh packets to the topic subscribers

        Args:
            packet  : Packet object

        """

        # Get all subscribers and remove the publisher
        subscribers = self.register.get_subscribers(packet.topic)

        # Publish to all subscribers
        for subscriber in subscribers:

            # Skip the sender of the message
            if self.client == subscriber:
                continue

            # Send the message to the rest of the subscribers
            try:
                self.log.debug("PUBLISH to {0} with topic='{1}', data={2}".format(
                                subscriber.getpeername(),
                                packet.topic,
                                tuple(packet.data)
                            ))
                subscriber.sendall(packet.to_bytes())

            except socket.error:
                self.log.debug("Client not accessible, deleting fromt the register")
                self.register[packet.topic].remove(subscriber)

    ###############################################################################################

    def update(self, packet):
        """ Update the session state

        Args:
            packet  : Packet object

        """

        # STATE: WAIT_CONNECT
        if self.state == self.WAIT_CONNECT:

            # Request to connect to the broker
            if packet.id == ConnectPacket.ID:
                self.log.debug('CONNECT from {0}'.format(self.client.getpeername()))
                self.state = self.CONNECTED

            # Ignore packets until the connect packet is detected
            else:
                self.log.debug("UNEXPECTED PACKET {0} in state {1}".format(packet, self.state))

        # STATE: CONNECTED
        elif self.state == self.CONNECTED:

            # Request to disconnect from the broker
            if packet.id == DisconnectPacket.ID:
                self.log.debug('DISCONNECT from {0}'.format(self.client.getpeername()))
                self.terminate.set()

            # Perform the required operations on other packets
            else:
                self.on_packet(packet)

    ###############################################################################################

    def listen(self):
        """ Wait for new data and write it to the input stream """

        while not self.terminate.is_set():

            with self.lock:
                stream_length = len(self.stream_in)

            # self.log.debug("STREAM LENGT = {0}".format(stream_length))

            try:
                if stream_length < MAX_STREAM_SIZE:
                    data = self.client.recv(BUFFER_SIZE)
                    with self.lock:
                        self.stream_in += data

            # Ingore errors when the recv call did not return data on time
            except socket.error as e:
                if e.errno != self.ERROR_NO_DATA:
                    self.stop()

    ###############################################################################################

    def run(self):
        """ Session activity required by threading.Thread on start()

         1. Register the current session
         2. Start the message sniffer
         3. While stop signal not active
             3.1. Copy the input buffer
             3.2. Parse a packet from the buffer
             3.3. Update the session state

        """

        self.log.debug("SESSION START")
        self.register.subscribe(self)

        # Start the data capture thread
        listener = threading.Thread(target=self.listen)
        listener.start()

        while not self.terminate.is_set():
            try:
                with self.lock:

                    # Parse a packet from the stream
                    packet = Packet.from_bytes(self.stream_in)

                    # Remove the packet bytes from the stream
                    self.stream_in = self.stream_in[len(packet):]

                # Update the session state
                self.update(packet)

            except HvlpParsingError:
                pass

        self.cleanup()
        self.log.debug("SESSION END")

    ###############################################################################################

    def stop(self):
        """ Stop the current thread """
        self.terminate.set()

    ###############################################################################################

    def cleanup(self):
        """ Close the client connection and remove the session from the register """

        try:
            # Close the client connection
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()

            # Remove session from the register
            self.register.unsubscribe(self)

            # Show the register before
            self.log.debug("Register before : {0}".format(self.register.get_sessions()))

            # Remove the client connection from the registry
            for topic in self.register.keys():
                if self.client in self.register[topic]:
                    self.register[topic].remove(self.client)

            # Show the register after
            self.log.debug("Register after : {0}".format(self.register.get_sessions()))

        except socket.error:
            pass
