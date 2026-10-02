import logging
import threading
from queue import Empty, Queue

from lib.common.constants import (
    ACTION_DOWNLOAD,
    ACTION_UPLOAD,
    QUEUE_TIMEOUT,
    RECEIVER_TIMEOUT,
    REQUEST_SIZE,
    TYPE_ACK,
    TYPE_CONFIRM,
    TYPE_START,
)
from lib.common.packet_utils import decode, encode
from lib.common.request_utils import parse_request
from lib.server.downloadHandler import DownloadHandler
from lib.server.logMessages import (
    ERROR_CLIENTHANDLER,
    ERROR_FORMAT_REQUEST,
    ERROR_UNKNOWN_ACTION,
    EXECUTE_ACTION,
)
from lib.server.uploadHandler import UploadHandler

logger = logging.getLogger(__name__)

ACTIONS = {
    ACTION_UPLOAD: UploadHandler,
    ACTION_DOWNLOAD: DownloadHandler,
}


class ClientHandler(threading.Thread):
    def __init__(self, addr, server_socket, storage, finish):
        super().__init__(daemon=True)
        self.socket = server_socket
        self.addr = addr
        self.finish = finish
        self.storage = storage
        self.queue = Queue()

    def run(self):
        self.handle()

    def _wait_for_start(self):  # Hanshake
        result = ()
        while True:
            try:
                """timeout=QUEUE_TIMEOUT, si pasan 10 segundos sin nada,
                .get() lanza Empty, el except lo convierte en return None,
                handle() cae al finally y libera todo"""
                request = self.queue.get(timeout=QUEUE_TIMEOUT)
            except Empty:
                return None

            pack_type, _, payload = decode(request)
            if pack_type == TYPE_START:
                parts = parse_request(payload)
                if len(parts) != REQUEST_SIZE:
                    logger.error(ERROR_FORMAT_REQUEST.format(addr=self.addr))
                    continue
                result = parts
                packet = encode(TYPE_ACK)
                self.send_packet(packet)
                continue

            if (
                pack_type == TYPE_CONFIRM
            ):  # Tenemos QUEUE_TIMEOUT=10s para recibir el confirm
                return result  # handshake completo

    def recv_data(self, data):
        self.queue.put(data)

    def get_packet(self, timeout=RECEIVER_TIMEOUT):
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            raise TimeoutError

    def send_packet(self, packet):
        self.socket.sendto(packet, self.addr)

    def handle(self):
        try:
            result = self._wait_for_start()
            if not result:
                return
            action, filename, protocol = result
            logger.info(
                EXECUTE_ACTION.format(
                    addr=self.addr,
                    action=action,
                    filename=filename,
                    protocol=protocol.upper(),
                )
            )
            handler_cls = ACTIONS.get(action)
            if not handler_cls:
                logger.error(ERROR_UNKNOWN_ACTION.format(addr=self.addr,
                                                         action=action))
                return
            handler_cls(self).execute(self.storage, filename, protocol)
        except Exception as error:
            logger.error(ERROR_CLIENTHANDLER.format(addr=self.addr, err=error))
        finally:
            self.finish(self.addr)
