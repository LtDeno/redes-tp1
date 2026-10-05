import logging
from time import sleep

from lib.common.constants import (READY_DELAY, READY_BURST, MAX_RETRIES,
                                  DELAY, TYPE_ERROR, TYPE_READY)
from lib.common.fileHandler import FileHandler
from lib.common.packet_utils import encode
from lib.common.protocols import PROTOCOLS
from lib.server.logMessages import ERROR_READ_FILE, SENDING_FILE, SENT_FILE, FIN_NOT_CONFIRMED

logger = logging.getLogger(__name__)


class DownloadHandler:
    def __init__(self, ctx):
        self.ctx = ctx  # referencia al ClientHandler

    """Se agrega un agregar un delay entre reintentos
    para que no se disparén todos juntos"""

    def _send_ready(self):
        for i in range(READY_BURST):
            packet = encode(TYPE_READY)
            self.ctx.send_packet(packet)
            if i < READY_BURST - 1:  # Cuando se envia el ult ready, no duerme
                sleep(READY_DELAY)

    def _send_error(self):
        for _ in range(MAX_RETRIES):
            packet = encode(TYPE_ERROR)
            self.ctx.send_packet(packet)
            sleep(DELAY)  # medio segundo entre cada envío

    def execute(self, storage, filename, protocol):
        file_handler = FileHandler(storage, filename)
        data = file_handler.read()
        if not data:
            logger.error(ERROR_READ_FILE.format(addr=self.ctx.addr,
                                                filename=filename))
            self._send_error()
            return

        self._send_ready()
        logger.info(SENDING_FILE.format(addr=self.ctx.addr,
                                        filename=filename))
        protocol_instance = PROTOCOLS[protocol](self.ctx)
        if not protocol_instance.send_data(data):
            logger.warning(FIN_NOT_CONFIRMED.format(max_retries=MAX_RETRIES, chunks=len(data)))
        logger.info(SENT_FILE.format(addr=self.ctx.addr, filename=filename))
    
