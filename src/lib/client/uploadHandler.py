import logging
from time import monotonic

from lib.client.client import Client
from lib.client.logMessages import (
    ERROR_FILE,
    ERROR_TRANSFER,
    FAIL_CONNECTION,
    INIT_TRANS_DATA,
    REQUEST_UPLOAD,
    SUCCESSFUL_UPLOAD,
    TIMEOUT_ACK,
    TIMEOUT_READY,
    FIN_NOT_CONFIRMED
)
from lib.common.constants import (
    ACTION_UPLOAD,
    HANDSHAKE_RETRIES,
    MAX_RETRIES,
    READY_WINDOW,
    CONFIRM_TIMEOUT,
    TYPE_ACK,
    TYPE_CONFIRM,
    TYPE_READY,
    TYPE_START,
)
from lib.common.fileHandler import FileHandler
from lib.common.packet_utils import decode, encode
from lib.common.protocols import PROTOCOLS
from lib.common.request_utils import build_request

logger = logging.getLogger(__name__)


class UploadHandler:
    def __init__(self, args):
        self.filename = args.name
        self.src = args.src
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
        """ "" True = READY, None = no llegó nada."""
        limit = monotonic() + READY_WINDOW
        while True:
            remaining = limit - monotonic()
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
            except TimeoutError:
                if limit - monotonic() <= 0:
                    return None
                packet = encode(TYPE_CONFIRM)
                self.client.send_packet(packet)

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

        # Fase 2: CONFIRM -> READY
        packet = encode(TYPE_CONFIRM)
        self.client.send_packet(packet)
        resultado = self._wait_for_ready()
        if resultado is None:
            logger.warning(TIMEOUT_READY)
        return resultado

    def _transfer_file(self, data):
        logger.info(INIT_TRANS_DATA)
        try:
            protocol = PROTOCOLS[self.protocol](self.client)
            if not protocol.send_data(data):
                logger.warning(FIN_NOT_CONFIRMED.format(max_retries=MAX_RETRIES, chunks=len(data))) 
            logger.info(SUCCESSFUL_UPLOAD.format(filename=self.filename))
        except Exception as e:
            logger.error(ERROR_TRANSFER.format(error=e))
        finally:
            self.client.finish()

    def execute(self):
        file = FileHandler(self.src, self.filename)
        data = file.read()
        if not data:
            logger.error(ERROR_FILE.format(filename=self.filename))
            return

        logger.info(REQUEST_UPLOAD.format(filename=self.filename))
        request = build_request(ACTION_UPLOAD, self.filename, self.protocol)
        result = self._handshake(request)
        if result is None:
            logger.error(FAIL_CONNECTION)
            self.client.finish()
            return
        self._transfer_file(data)
