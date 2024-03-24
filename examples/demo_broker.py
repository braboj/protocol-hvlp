from __future__ import print_function
from __future__ import unicode_literals

from hvlp.broker import *
from hvlp.logger import *
import socket

configure_logger()

# Spawn several brokers as threads
brokers = []
for i in range(10):
    broker = HvlpBroker(port=65000 + i)
    broker.start()
    brokers.append(broker)

# Attempt connection to the broker instances
for broker in brokers:
    sock = socket.socket()
    sock.connect((broker.ip_addr, broker.port))
    sock.close()

# Stop all broker instances
for broker in brokers:
    broker.stop()
