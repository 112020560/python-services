from abc import ABCMeta, abstractmethod


class MessageBrokerInterface(metaclass=ABCMeta):
    @abstractmethod
    def publish(self, event, message):
        raise NotImplementedError
