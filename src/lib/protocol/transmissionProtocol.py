from __future__ import annotations
import logging
import time
from abc import ABC, abstractmethod

from lib.common.constants import (
    DATA_LISTENER_TIMEOUT,
    MAX_RETRIES,
    TYPE_FIN,
    TYPE_FIN_ACK,
)
from lib.common.packet_utils import decode, encode
from lib.protocol.logMessages import (
    ERROR_FIN_ACK,
    RECV_FIN,
    RECV_FIN_ACK,
    RECV_FIN_RETRANSMIT,
    SEND_FIN,
)

logger = logging.getLogger(__name__)


class TransmissionProtocol(ABC):
    def __init__(self, context, timeout):
        self.ctx = context  # referencia a ClientHandler o Client
        self.timeout = timeout

    def _recv_fin(self):
        logger.debug(RECV_FIN)
        packet_fin_ack = encode(TYPE_FIN_ACK)
        self.ctx.send_packet(packet_fin_ack)
        # Para seguir respondiendo FINs reenviados
        deadline = time.monotonic() + self.timeout * 2
        while time.monotonic() < deadline:
            try:
                packet = self.ctx.get_packet(timeout=DATA_LISTENER_TIMEOUT)
                if decode(packet)[0] == TYPE_FIN:
                    logger.debug(RECV_FIN_RETRANSMIT)
                    self.ctx.send_packet(encode(TYPE_FIN_ACK))
            except TimeoutError:
                continue

    def _send_fin(self):
        fin_packet = encode(TYPE_FIN)
        for cont_retries in range(1, MAX_RETRIES + 1):
            self.ctx.send_packet(fin_packet)
            logger.debug(SEND_FIN.format(num=cont_retries))
            try:
                ack_packet = self.ctx.get_packet(timeout=self.timeout)
                packet_type, _, _ = decode(ack_packet)
                if packet_type == TYPE_FIN_ACK:
                    logger.debug(RECV_FIN_ACK)
                    return True
            except TimeoutError:
                continue
        logger.warning(ERROR_FIN_ACK.format(max_retries=MAX_RETRIES))
        return False

    @abstractmethod
    def send_data(self, chunks: list[bytes]) -> bool:
        pass

    @abstractmethod
    def receive_data(self, chunks: list[bytes]) -> bool:
        pass
