from abc import ABC, abstractmethod


class TransmissionProtocol(ABC):
    @abstractmethod
    def send_data(self, chunks: list[bytes]):
        pass

    @abstractmethod
    def receive_data(self, chunks: list[bytes]):
        pass
