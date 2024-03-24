# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import sys
sys.path.append(str('.'))
sys.path.append(str('..'))

from packets import *
from logger import *


###################################################################################################
# MODULE TESTS
###################################################################################################

def test_packet(payload=(1, 2, 3, 4, 5)):

    packet = Packet(packet_id=7, payload=payload)
    logging.info("@PACKET")
    logging.info("PAYLOAD = {0}".format(payload))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


def test_connect(payload=(1, 2, 3, 4, 5)):

    packet = ConnectPacket(payload)
    logging.info("@CONNECT")
    logging.info("PAYLOAD = {0}".format(payload))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


def test_disconnect(payload=(1, 2, 3, 4, 5)):

    packet = DisconnectPacket(payload)
    logging.info("@DISCONNECT")
    logging.info("PAYLOAD = {0}".format(payload))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


def test_subscribe(topics=('здравей', 'home')):

    packet = SubscribePacket(topics)
    logging.info("@SUBSCRIBE")
    logging.info("TOPICS = {0}".format(topics))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


def test_unsubscribe(topics=('здравей', 'home')):

    packet = UnsubscribePacket(topics)
    logging.info("@UNSUBSCRIBE")
    logging.info("TOPICS = {0}".format(topics))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


def test_publish(topic='здравей', data=(0xAA, 0x55)):

    packet = PublishPacket(topic, data)
    logging.info("@PUBLISH")
    logging.info("TOPIC = '{0}' DATA = {1}".format(topic, data))

    # Serialize packet
    serialized = tuple(packet.to_bytes())
    logging.info("SERIALIZED = {0}".format(serialized))

    # Deserialize packet
    deserialized = Packet.from_bytes(serialized)
    logging.info("DESERIALIZED = {0}".format(deserialized))

    assert(packet == deserialized)


###################################################################################################
# MAIN
###################################################################################################

if __name__ == "__main__":

    configure_logger()
    test_packet()
    test_connect()
    test_disconnect()
    test_subscribe()
    test_unsubscribe()
    test_publish()
