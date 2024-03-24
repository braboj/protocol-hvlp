# coding: utf-8
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from hvlp.broker import *
from hvlp.client import *
from hvlp.logger import *

import time


def test_connect():

    broker = HvlpBroker(port=65000)
    broker.start()
    register = broker.register

    # Perform the TCP handhsake
    client = HvlpClient(port=65000)
    client.open()
    time.sleep(1)

    # Get the last registered session
    session = register.get_sessions()[-1]

    # Check the session state after the TCP handshake
    assert (session.state == HvlpSession.WAIT_CONNECT and session.is_alive())
    print(session.state)

    # Send the CONNECT packet to the broker
    client.connect()
    time.sleep(1)

    # Check the session state after the CONNECT packet
    assert (session.state == HvlpSession.CONNECTED and session.is_alive())
    print(session.CONNECTED)

    broker.stop()
    broker.join()


def test_disconnect():

    broker = HvlpBroker(port=65001)
    broker.start()
    register = broker.register

    # Perform the TCP handhsake
    client = HvlpClient(port=65001)

    # Open the connection
    client.open()
    time.sleep(1)

    # Get the last registered session
    session = register.get_sessions()[-1]

    # Send a connect packet to the broker
    client.connect()
    time.sleep(1)

    # Send a disconnect packet to the broker
    client.disconnect()
    time.sleep(1)

    # The sessions must not be alive after disconnect
    assert (not session.is_alive())

    broker.stop()
    broker.join()


def test_subscribe():

    broker = HvlpBroker(port=65002)
    broker.start()
    register = broker.register

    # Perform the TCP handhsake
    client = HvlpClient(port=65002)

    # Open the connection
    client.open()
    time.sleep(1)

    # Get the last registered session
    session = register.get_sessions()[-1]

    # Send a connect packet to the broker
    client.connect()
    time.sleep(1)

    # Send a subscribe packet to the broker
    client.subscribe('test')
    time.sleep(1)

    topics = register.get_topics(client=session.client)
    assert ('test' in topics)

    # Send a disconnect packet to the broker
    client.disconnect()
    time.sleep(1)

    broker.stop()
    broker.join()


###################################################################################################
# MAIN
###################################################################################################

if __name__ == "__main__":
    configure_logger()
    test_connect()
    test_disconnect()
    test_subscribe()
