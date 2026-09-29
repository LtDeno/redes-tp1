from abc import ABC, abstractmethod

class ProtocolTransmission(ABC):
    @abstractmethod
    def send_data(self, message):
        pass

    @abstractmethod
    def recieve_data(self, message):
        pass
