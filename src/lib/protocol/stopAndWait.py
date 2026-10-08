from __future__ import annotations
import logging
import time

from lib.common.constants import (
    SW_ACK_LISTENER_TIMEOUT,
    DATA_LISTENER_TIMEOUT,
    SW_TIMEOUT,
    SW_STALL_TIMEOUT,
    IDLE_TIMEOUT,
    TYPE_ACK,
    TYPE_DATA,
    TYPE_FIN,
)
from lib.common.packet_utils import decode, encode
from lib.protocol.logMessages import (
    DISCARD_DUP,
    NO_DATA_RECEIVED,
    RECV_ACK_DATA,
    RECV_DATA,
    SEND_ACK_DATA,
    SEND_DATA_PACKET,
    ERROR_SEND_STALL,
    TRANSFER_INCOMPLETE,
)
from lib.protocol.transmissionProtocol import TransmissionProtocol

logger = logging.getLogger(__name__)


class Sender:
    def __init__(self):
        self.seq_num = 0
        self.abs_seq_num = 0  # index de chunk


class Receiver:
    def __init__(self, fin_timeout: float):
        self.expected_seq_num = 0  # Contador absoluto de lo que se espera
        self.receive = True  # Seguir escuchando/recibiendo
        self.last_received_time = (
            time.monotonic()
        )  # Para asumir si el emisor se "murio"
        self.fin_timeout = fin_timeout  # Para asumir si el emisor se "murio"

    def punch_clock(self):
        """Reinicia el reloj de inactividad en cada paquete recibido."""
        self.last_received_time = time.monotonic()

    def check_fin_timeout(self):
        idle_too_long = (time.monotonic()
                         - self.last_received_time > self.fin_timeout)
        # received_data = self.expected_seq_num > 0
        # if idle_too_long and received_data:
        # self.receive = False
        if not idle_too_long:
            return
        self.receive = False


class StopAndWait(TransmissionProtocol):
    def __init__(self, context):
        super().__init__(context, SW_TIMEOUT)

    def send_data(self, chunks):
        sender = Sender()
        total_chunks = len(chunks)
        if total_chunks == 0:
            chunks = [b""]
            total_chunks = 1

        while sender.abs_seq_num < total_chunks:
            wrapped_seq_num = sender.seq_num % 2
            packet = encode(TYPE_DATA, wrapped_seq_num,
                            chunks[sender.abs_seq_num])

            packet_acknowledged = False
            stall_deadline = time.monotonic() + SW_STALL_TIMEOUT
            while not packet_acknowledged:

                """Para chequear si debemos seguir enviando"""
                if(time.monotonic() > stall_deadline):
                    logger.error(ERROR_SEND_STALL.format(
                        timeout=self.stall_timeout,
                        confirmed=sender.send_base,
                        total=total_chunks))
                    return False
                "-------------------------------------------"

                self.ctx.send_packet(packet)
                logger.debug(SEND_DATA_PACKET.format(seq_num=wrapped_seq_num))
                
                start_time = time.monotonic()
                while time.monotonic() - start_time < self.timeout:
                    try:
                        ack_packet = self.ctx.get_packet(timeout=SW_ACK_LISTENER_TIMEOUT)
                        packet_type, ack_num, _ = decode(ack_packet)
                        if (packet_type == TYPE_ACK
                                and ack_num == wrapped_seq_num):
                            logger.debug(RECV_ACK_DATA.format(seq_num=ack_num))
                            packet_acknowledged = True
                            break
                    except TimeoutError:
                        pass

                if packet_acknowledged:
                    break

            sender.abs_seq_num += 1
            sender.seq_num += 1

        return self._send_fin()

    def receive_data(self, chunks):
        receiver = Receiver(IDLE_TIMEOUT) #Receiver(self.timeout * 3)
        while receiver.receive:
            try:
                packet = self.ctx.get_packet(timeout=DATA_LISTENER_TIMEOUT)
                receiver.punch_clock()
                packet_type, seq_num, payload = decode(packet)

                if packet_type == TYPE_FIN:
                    self._recv_fin()
                    receiver.receive = False
                    return True

                elif packet_type == TYPE_DATA and seq_num is not None:
                    wrapped_seq_num = receiver.expected_seq_num % 2
                    ack_packet = encode(TYPE_ACK, seq_num)
                    logger.debug(SEND_ACK_DATA.format(seq_num=seq_num))
                    self.ctx.send_packet(ack_packet)

                    if seq_num == wrapped_seq_num:
                        logger.debug(RECV_DATA.format(seq_num=seq_num))
                        chunks.append(b"" if payload is None else payload)
                        receiver.expected_seq_num += 1
                    else:
                        logger.debug(
                            DISCARD_DUP.format(
                                seq_num=seq_num, expected=wrapped_seq_num
                            )
                        )

            except TimeoutError:
                pass

            receiver.check_fin_timeout()
        # salir del while = timeout -> Salir del while solo
        # puede ser por check_fin_timeout
        if receiver.expected_seq_num == 0:
            logger.error(NO_DATA_RECEIVED.format(timeout=receiver.fin_timeout))
        else:
            logger.error(
                TRANSFER_INCOMPLETE.format(
                    timeout=receiver.fin_timeout,
                    received=receiver.expected_seq_num
                )
            )
        return False
