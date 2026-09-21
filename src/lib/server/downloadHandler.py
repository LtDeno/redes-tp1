import logging
from time import sleep

from src.lib.common.constants import DELAY, MAX_RETRIES, TYPE_ERROR, TYPE_READY
from src.lib.common.fileHandler import FileHandler
from src.lib.common.logMessages import ERROR_READ_FILE, SENDING_FILE, SENT_FILE
from src.lib.common.packet_utils import encode
from src.lib.common.protocols import PROTCOLS

logger = logging.getLogger(__name__)


class DownloadHandler:
    def __init__(self, ctx):
        self.ctx = ctx  # referencia al ClientHandler

    """Se agrega un agregar un delay entre reintentos para que no se disparén todos juntos"""

    def _send_ready(self):
        for _ in range(MAX_RETRIES):
            packet = encode(TYPE_READY, 0)
            self.ctx.send_packet(packet)
            sleep(DELAY)  # medio segundo entre cada envío

    def _send_error(self):
        for _ in range(MAX_RETRIES):
            packet = encode(TYPE_ERROR, 0)
            self.ctx.send_packet(packet)
            sleep(DELAY)  # medio segundo entre cada envío

    def execute(self, storage, filename, protocol):
        file_handler = FileHandler(storage, filename)
        data = file_handler.read()
        if not data:
            logger.error(ERROR_READ_FILE.format(addr=self.ctx.addr, filename=filename))
            self._send_error()
            return

        self._send_ready()
        logger.info(SENDING_FILE.format(addr=self.ctx.addr, filename=filename))
        protocol_instance = PROTCOLS[protocol](self.ctx)
        protocol_instance.send_file(data)
        logger.info(SENT_FILE.format(addr=self.ctx.addr, filename=filename))
