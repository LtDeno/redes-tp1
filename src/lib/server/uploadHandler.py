import logging
from time import sleep

from src.lib.common.constants import DELAY, MAX_RETRIES, TYPE_READY
from src.lib.common.fileHandler import FileHandler
from src.lib.common.logMessages import RECEIVING_FILE, SAVE_FILE
from src.lib.common.packet_utils import encode
from src.lib.common.protocols import PROTCOLS

logger = logging.getLogger(__name__)


class UploadHandler:
    def __init__(self, ctx):
        self.ctx = ctx  # referencia al ClientHandler

    def _send_ready(self):
        for _ in range(MAX_RETRIES):
            packet = encode(TYPE_READY, 0)
            self.ctx.send_packet(packet)
            sleep(DELAY)  # medio segundo entre cada envío

    def execute(self, storage, filename, protocol):
        self._send_ready()
        logger.info(RECEIVING_FILE.format(addr=self.ctx.addr, filename=filename))
        data = []
        protocol_instance = PROTCOLS[protocol](self.ctx)
        protocol_instance.receive_file(data)

        file_handler = FileHandler(storage, filename)
        file_handler.write(data)
        logger.info(SAVE_FILE.format(addr=self.ctx.addr, filename=filename))
