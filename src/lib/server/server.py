import logging
import socket
import threading
from os import makedirs

from src.lib.common.logMessages import (
    CLIENT_REMOVED,
    NEW_CLIENT,
    SERVER_LISTENING,
    SERVER_SHUTDOWN,
)

from .clientHandler import ClientHandler

HOST = 0
PORT = 1
logger = logging.getLogger(__name__)


class Server:
    def __init__(self, address, storage):
        self.addr = address
        self.storage = storage
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket UDP
        self.clients = {}
        self.lock = threading.Lock()

    def _create_storage(self):
        makedirs(self.storage, exist_ok=True)

    def _remove_client(self, addr):
        with self.lock:
            if addr in self.clients:
                del self.clients[addr]
                logger.info(CLIENT_REMOVED.format(addr=addr))

    def _process_client(self, data, addr):
        if addr not in self.clients:
            logger.info(NEW_CLIENT.format(addr=addr))
            self.clients[addr] = ClientHandler(
                addr, self.socket, self.storage, self._remove_client
            )
            self.clients[addr].recv_packet(data)
            self.clients[addr].start()
        else:
            self.clients[addr].recv_packet(data)

    def start(self):
        self._create_storage()
        self.socket.bind(self.addr)
        logger.info(SERVER_LISTENING.format(host=self.addr[HOST], port=self.addr[PORT]))

        while True:
            try:
                data, addr = self.socket.recvfrom(4096)
                with self.lock:
                    self._process_client(data, addr)
            except TimeoutError:
                continue
            except KeyboardInterrupt:
                logger.info(SERVER_SHUTDOWN)
                break
        self.socket.close()
