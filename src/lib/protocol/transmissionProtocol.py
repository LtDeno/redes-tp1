from abc import ABC, abstractmethod


class TransmissionProtocol(ABC):
    @abstractmethod
    def send_data(self, message):
        pass

    @abstractmethod
    def receive_data(self, message):
        pass
