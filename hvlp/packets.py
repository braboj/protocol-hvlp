# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from hvlp.errors import *


class Packet(object):
    """ Generic template packet class

    This class defines the common structure of the packet.

        ID          #   1 Byte
        LENGTH      #   1 Byte
        PAYLOAD     #   Up to 255 Bytes

    """

    ID_OFFSET = 0
    LENGTH_OFFSET = 1
    PAYLOAD_OFFSET = 2

    def __init__(self, packet_id, payload):
        self.id = packet_id
        self.length = len(payload)
        self.payload = bytearray(payload)

    def __len__(self):
        """ Return the object length """
        return self.length + 2

    def __eq__(self, other):
        """ Implementation of the '==' operator """

        result = \
            (self.id == other.id) and \
            (self.length == other.length) and \
            (self.payload == other.payload)

        return result

    def __ne__(self, other):
        """ Implementation of the '!=' operator """

        result = not (self.__eq__(other))
        return result

    def __str__(self):
        """ String representation of the object """

        packet_id = str(self.id)
        length = str(self.length)
        payload = self.payload
        message = "PACKET ID: {0} | LEN={1} | PAYLOAD={2}".format(packet_id, length, tuple(payload))
        return message

    def to_bytes(self):
        """ Serialize the packet object """

        stream = [self.id, self.length]
        stream.extend(self.payload)
        return bytearray(stream)

    @classmethod
    def from_bytes(cls, stream):
        """ Deserialize the packet object """

        try:

            # Convert stream
            stream = bytearray(stream)

            # Read the packet ID and remove it from the stream
            packet_id = stream[cls.ID_OFFSET]
            length = stream[cls.LENGTH_OFFSET]
            payload = stream[cls.PAYLOAD_OFFSET:(length + cls.PAYLOAD_OFFSET)]

            # Connect packet
            if packet_id == ConnectPacket.ID:
                packet = ConnectPacket.from_bytes(payload)

            # Disconnect packet
            elif packet_id == DisconnectPacket.ID:
                packet = DisconnectPacket.from_bytes(payload)

            # Subcribe packet
            elif packet_id == SubscribePacket.ID:
                packet = SubscribePacket.from_bytes(payload)

            # Unsubscribe packet
            elif packet_id == UnsubscribePacket.ID:
                packet = UnsubscribePacket.from_bytes(payload)

            # Publish packet
            elif packet_id == PublishPacket.ID:
                packet = PublishPacket.from_bytes(payload)

            # Unknown packet
            else:
                packet = cls(packet_id=packet_id, payload=payload)

        # The stream is empty
        except IndexError:
            raise HvlpParsingError

        return packet


###################################################################################################

class ConnectPacket(Packet):
    """ Connect packet class

    The constructor is reponsible for the preparation of the payload.

    Args:
        payload:    Optional data to be sent by the CONNECT packet

    """

    ID = 1

    def __init__(self, payload=()):
        super(ConnectPacket, self).__init__(packet_id=self.ID, payload=payload)

    @classmethod
    def from_bytes(cls, payload):
        return cls(payload=payload)


###################################################################################################

class DisconnectPacket(Packet):
    """ Disconnect packet class

    The constructor is reponsible for the preparation of the payload.

    Args:
        payload:    Optional data to be sent by the DISCONNECT packet

    """

    ID = 2

    def __init__(self, payload=()):
        super(DisconnectPacket, self).__init__(packet_id=self.ID, payload=payload)

    @classmethod
    def from_bytes(cls, payload):
        return cls(payload=payload)


###################################################################################################

class SubscribePacket(Packet):
    """ Subscribe packet class

    The constructor is reponsible for the preparation of the payload.

    Args:
        topics:    A list of topic names

    """

    ID = 3

    def __init__(self, topics):

        self.topics = topics

        payload = []
        for topic in topics:
            topic_name = topic.encode('utf-8')
            topic_length = len(topic_name)
            payload.append(topic_length)
            payload.extend(topic_name)

        super(SubscribePacket, self).__init__(packet_id=self.ID, payload=payload)

    def __str__(self):
        """ String representation of the object """

        packet_id = str(self.id)
        length = str(self.length)
        payload = self.topics
        message = "PACKET ID: {0} | LEN={1} | PAYLOAD={2}".format(packet_id, length, payload)
        return message

    @classmethod
    def from_bytes(cls, payload):

        topics = []
        while payload:

            # Extract the next topic length and name
            topic_len = payload[0]
            topic_name = payload[1:topic_len + 1]

            # Remove the topic string from the payload
            payload = payload[topic_len + 1:]
            topics.append(topic_name.decode('utf-8'))

        return cls(topics=topics)


###################################################################################################

class UnsubscribePacket(Packet):
    """ Unsubscribe packet class

    The constructor is reponsible for the preparation of the payload.

    Args:
        topics:    A list of topic names

    """

    ID = 4

    def __init__(self, topics):

        self.topics = topics

        payload = []
        for topic in topics:
            topic_name = topic.encode('utf-8')
            topic_length = len(topic_name)
            payload.append(topic_length)
            payload.extend(topic_name)

        super(UnsubscribePacket, self).__init__(packet_id=self.ID, payload=payload)

    def __str__(self):
        """ String representation of the object """

        packet_id = str(self.id)
        length = str(self.length)
        payload = self.topics
        message = "PACKET ID: {0} | LEN={1} | PAYLOAD={2}".format(packet_id, length, payload)
        return message

    @classmethod
    def from_bytes(cls, payload):

        topics = []
        while payload:

            # Extract the next topic length and name
            topic_len = payload[0]
            topic_name = payload[1:topic_len + 1]

            # Remove the topic string from the payload
            payload = payload[topic_len + 1:]
            topics.append(topic_name.decode('utf-8'))

        return cls(topics=topics)

###################################################################################################


class PublishPacket(Packet):
    """ Publish packet class

    The constructor is reponsible for the preparation of the payload.

    Args:
        topic   : Topic name
        data    : Array of bytes to publish

    """

    ID = 5

    def __init__(self, topic, data):

        self.topic = topic
        self.data = data

        encoded_topic = self.topic.encode('utf-8')
        payload = [len(encoded_topic)]
        payload.extend(encoded_topic)
        payload.extend(data)

        super(PublishPacket, self).__init__(packet_id=self.ID, payload=payload)

    def __str__(self):
        """ String representation of the object """

        packet_id = str(self.id)
        length = str(self.length)
        payload = [self.topic]
        payload.extend(tuple(self.data))
        message = "PACKET ID: {0} | LEN={1} | PAYLOAD={2}".format(packet_id, length, payload)
        return message

    @classmethod
    def from_bytes(cls, payload):

        topic_len = payload[0]
        topic_name = payload[1:topic_len + 1]
        data = payload[topic_len + 1:]

        return cls(topic=topic_name.decode('utf-8'), data=data)
