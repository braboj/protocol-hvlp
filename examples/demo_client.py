# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from hvlp.broker import *
from hvlp.client import *
from hvlp.packets import *
from hvlp.errors import *
from hvlp.logger import *

import threading
import sys

sys.path.append(str('.'))
sys.path.append(str('..'))


###################################################################################################

def producer(n=0):
    test_client = HvlpClient()
    test_client.open()
    test_client.connect()
    test_client.subscribe('a')

    i = 0
    while True:
        test_client.publish('a', (i % 256))
        if n and i > n:
            break
        i += 1


###################################################################################################

def consumer(stop):
    test_client = HvlpClient()

    test_client.open()
    test_client.connect()
    test_client.subscribe('a')

    t = threading.Thread(target=test_client.listen, args=(stop,))
    t.start()

    while not stop.is_set():
        try:
            packet = Packet.from_bytes(test_client.stream_in)
            test_client.stream_in = test_client.stream_in[len(packet):]
            logging.info(packet)
        except HvlpParsingError:
            pass


###################################################################################################

configure_logger()

broker = HvlpBroker()
broker.start()

stop_flag = threading.Event()
stop_flag.clear()

p = threading.Thread(target=producer, args=[0])
p.start()

c = threading.Thread(target=consumer, args=[stop_flag, ])
c.start()

try:
    while True:
        pass

except KeyboardInterrupt:
    pass

stop_flag.set()
broker.stop()
