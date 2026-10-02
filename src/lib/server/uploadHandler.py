import logging
from time import sleep

from lib.common.constants import READY_DELAY, READY_BURST, TYPE_READY
from lib.common.fileHandler import FileHandler
from lib.common.packet_utils import encode
from lib.common.protocols import PROTOCOLS
from lib.server.logMessages import RECEIVING_FILE, SAVE_FILE
from lib.protocol.transmissionProtocol import TransmissionProtocol

logger = logging.getLogger(__name__)


class UploadHandler:
    def __init__(self, ctx):
        self.ctx = ctx  # referencia al ClientHandler

    def _send_ready(self):
        """Enviamos una ráfaga de 10, uno cada medio segundo,
        desde t=0 hasta t=4.5 s. Como UDP no garantiza entrega,
        si se pierde (o se tarda en llegar) el primero, hay otros 9."""
        for i in range(READY_BURST):
            packet = encode(TYPE_READY)
            self.ctx.send_packet(packet)
            if i < READY_BURST - 1:  # Cuando se envia el ult ready, no duerme
                sleep(READY_DELAY)

    def execute(self, storage, filename, protocol):
        self._send_ready()
        logger.info(RECEIVING_FILE.format(addr=self.ctx.addr,
                                          filename=filename))
        data = []
        protocol_instance: TransmissionProtocol = PROTOCOLS[protocol](self.ctx)
        protocol_instance.receive_data(data)

        file_handler = FileHandler(storage, filename)
        file_handler.write(data)
        logger.info(SAVE_FILE.format(addr=self.ctx.addr, filename=filename))
