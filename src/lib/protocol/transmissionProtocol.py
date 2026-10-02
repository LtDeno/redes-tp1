from abc import ABC, abstractmethod


class TransmissionProtocol(ABC):
    @abstractmethod
    def send_data(self, chunks: list[bytes]):
        pass

    @abstractmethod
    def recieve_data(self, chunks: list[bytes]):
        pass
