# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

import logging
import threading


class HvlpBrokerRegister(dict):
    """ Thread-safe register class for the HVLP broker """

    def __init__(self):
        super(HvlpBrokerRegister, self).__init__()
        self.__lock = threading.RLock()
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.addHandler(logging.NullHandler())
        self.__sessions = []

    ###############################################################################################

    def reset(self):
        """ Reset the register object. """

        with self.__lock:
            self.__sessions = []
            self.clear()

    ###############################################################################################

    def subscribe(self, session):
        """ Add an element as a new session.

        Args:
            session : Session object as a generic type

        """

        with self.__lock:
            self.__sessions.append(session)

    ###############################################################################################

    def unsubscribe(self, session):
        """ Add an element as a new session.

        Args:
            session : Session object as a generic type

        """

        with self.__lock:
            self.__sessions.remove(session)

    ###############################################################################################

    def append(self, topics, client):
        """ Add the client to the topics dictionary

        Args:
            topics  : Topic names
            client  : Client as a generic type

        """

        # Protected access
        with self.__lock:
            for topic in topics:
                subscribers = self.get_subscribers(topic)
                if client not in subscribers:
                    self.setdefault(topic, [])
                    self[topic].append(client)

    ###############################################################################################

    def remove(self, topics, client):
        """ Remove the client from the topics dictionary

        Args:
            topics  : Topic names
            client  : Client as a generic type

        """

        # Protected access
        with self.__lock:
            try:
                for topic in topics:

                    # Remove the client from the subscriber list
                    self[topic].remove(client)

                    # If no subscribers left, remove the topic
                    if not self[topic]:
                        self.pop(topic)

            except KeyError:
                self.__log.debug("Topic not found in register")

        self.__log.debug(self)

    ###############################################################################################

    def get_subscribers(self, topic):
        """ Get all the clients subscribed to a given topic

        Args:
            topic  : Topic name

        Returns:
            List of client connections subscribed to a given topic

        """

        result = []

        # Protected access
        with self.__lock:
            try:
                result.extend(self[topic])
            except KeyError:
                pass

        return result

    ###############################################################################################

    def get_topics(self, client):
        """ Get all the topics the client is subscribed to

        Args:
            client  : The client as a generic type

        Returns:
            List of subscriptions for a given client

        """

        result = []

        # Protected access
        with self.__lock:
            for topic, subscribers in self.items():
                if client in subscribers:
                    result.append(topic)

        return result

    ###############################################################################################

    def get_sessions(self):
        """ Get all registered client sessions

        Returns:
            List of sessions stored in the current register

        """

        with self.__lock:
            result = set(self.__sessions)

        return list(result)
