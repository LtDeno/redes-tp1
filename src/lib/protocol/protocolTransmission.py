from abc import ABC, abstractmethod


class ProtocolTransmission(ABC):
    @abstractmethod
    def send_file(self, chunks):
        pass

    @abstractmethod
    def receive_file(self, chunks):
        pass
