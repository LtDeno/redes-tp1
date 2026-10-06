import logging
from time import monotonic

from lib.client.client import Client
from lib.client.logMessages import (
    ERROR_TRANSFER,
    FAIL_CONNECTION,
    FILE_NOT_EXIST,
    INIT_RECV_DATA,
    REQUEST_DOWNLOAD,
    SUCCESSFUL_DOWNLOAD,
    TIMEOUT_ACK,
    TIMEOUT_READY,
)
from lib.common.constants import (
    ACTION_DOWNLOAD,
    HANDSHAKE_RETRIES,
    READY_WINDOW,
    CONFIRM_TIMEOUT,
    TYPE_ACK,
    TYPE_CONFIRM,
    TYPE_ERROR,
    TYPE_READY,
    TYPE_START,
)
from lib.common.fileHandler import FileHandler
from lib.common.packet_utils import decode, encode
from lib.common.protocols import PROTOCOLS
from lib.common.request_utils import build_request

logger = logging.getLogger(__name__)


class DownloadHandler:
    def __init__(self, args):
        self.filename = args.name
        self.dst = args.dst
        self.protocol = args.protocol
        self.client = Client(args.host, args.port)

    def _wait_for_ack(self):
        """Lee hasta obtener un ACK. Devuelve True/False."""
        try:
            packet = self.client.get_packet()
            pack_type, _, _ = decode(packet)
            if pack_type == TYPE_ACK:
                return True
        except TimeoutError:
            return False

    def _wait_for_ready(self):
        """True = READY, False = ERROR (archivo inexistente),
        None = no llegó nada."""
        limit = monotonic() + READY_WINDOW
        while True:
            remaining = limit - monotonic()  # cuánto t me queda de ventana
            if remaining <= 0:
                return None
            try:
                """ con timeout=min(remaining, CONFIRM_TIMEOUT) se evita
                que una espera se pase de la ventana total (Si quedan 0,4 s
                de ventana, espera 0,4 s y no 1 s)"""
                packet = self.client.get_packet(timeout=min(remaining,
                                                            CONFIRM_TIMEOUT))
                pack_type, _, _ = decode(packet)
                if pack_type == TYPE_READY:
                    return True
                if pack_type == TYPE_ERROR:
                    return False
            except TimeoutError:
                if limit - monotonic() <= 0:
                    return None
                packet = encode(TYPE_CONFIRM)
                self.client.send_packet(packet)
                continue

    def _handshake(self, request):
        for i in range(HANDSHAKE_RETRIES):
            # Fase 1: START -> ACK
            packet = encode(TYPE_START, payload=request)
            self.client.send_packet(packet)
            if self._wait_for_ack():
                break
            logger.warning(TIMEOUT_ACK.format(num=i + 1,
                                              max_retries=HANDSHAKE_RETRIES))
        else:
            return None

        # Fase 2: CONFIRM -> READY / ERROR
        packet = encode(TYPE_CONFIRM)
        self.client.send_packet(packet)
        resultado = self._wait_for_ready()
        if resultado is None:
            logger.warning(TIMEOUT_READY)
        return resultado

    def _receiving_file(self):
        logger.info(INIT_RECV_DATA)
        data = []
        file_handler = FileHandler(self.dst, self.filename)
        try:
            protocol = PROTOCOLS[self.protocol](self.client)
            if not protocol.receive_data(data):
                return
            file_handler.write(data)
            logger.info(
                SUCCESSFUL_DOWNLOAD.format(filename=self.filename,
                                           dst=self.dst)
            )
        except Exception as e:
            logger.error(ERROR_TRANSFER.format(error=e))
        finally:
            self.client.finish()

    def execute(self):
        logger.info(REQUEST_DOWNLOAD.format(filename=self.filename))
        request = build_request(ACTION_DOWNLOAD, self.filename, self.protocol)

        resultado = self._handshake(request)
        if resultado is None:
            logger.error(FAIL_CONNECTION)
            self.client.finish()
            return
        if not resultado:
            logger.error(FILE_NOT_EXIST.format(filename=self.filename))
            self.client.finish()
            return

        self._receiving_file()
