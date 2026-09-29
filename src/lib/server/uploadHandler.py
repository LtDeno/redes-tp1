import logging
from time import sleep

from lib.common.constants import DELAY, MAX_RETRIES, TYPE_READY
from lib.common.fileHandler import FileHandler
from lib.common.packet_utils import encode
from lib.common.protocols import PROTCOLS
from lib.server.logMessages import RECEIVING_FILE, SAVE_FILE

logger = logging.getLogger(__name__)


class UploadHandler:
    def __init__(self, ctx):
        self.ctx = ctx  # referencia al ClientHandler

    def _send_ready(self):
        """Enviamos una ráfaga de 10, uno cada medio segundo,
        desde t=0 hasta t=4.5 s. La idea: como UDP no garantiza entrega,
        si se pierde (o se tarda en llegar) el primero, hay otros 9."""
        for _ in range(MAX_RETRIES):
            packet = encode(TYPE_READY, 0)
            self.ctx.send_packet(packet)
            sleep(DELAY)  # medio segundo entre cada envío

    def execute(self, storage, filename, protocol):
        self._send_ready()
        logger.info(RECEIVING_FILE.format(addr=self.ctx.addr, filename=filename))
        data = []
        protocol_instance = PROTCOLS[protocol](self.ctx)
        protocol_instance.recieve_data(data) 

        file_handler = FileHandler(storage, filename)
        file_handler.write(data)
        logger.info(SAVE_FILE.format(addr=self.ctx.addr, filename=filename))
