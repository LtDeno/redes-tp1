from __future__ import annotations
import time
import logging
from lib.protocol.transmissionProtocol import TransmissionProtocol
from lib.common.constants import (
    WINDOW_SIZE,
    SR_TIMEOUT,
    SR_STALL_TIMEOUT,
    IDLE_TIMEOUT,
    SR_ACK_LISTENER_TIMEOUT,
    TYPE_DATA,
    TYPE_ACK,
    TYPE_FIN,
    DATA_LISTENER_TIMEOUT,
   
)
from lib.protocol.logMessages import (
    DISCARD_DUP,
    NO_DATA_RECEIVED,
    RECV_ACK_DATA,
    SEND_ACK_DATA,
    SEND_DATA_PACKET,
    WINDOW_SLIDE,
    RETRY_DATA,
    TRANSFER_INCOMPLETE,
    STALE_ACK,
    ERROR_SEND_STALL
)
from lib.common.packet_utils import encode, decode
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UnAckedPacket:
    packet: bytes
    time: float
    seq_num: int


class Sender:
    def __init__(self):
        self.send_base = 0
        self.next_seq_num = 0
        self.buffer: dict[int, UnAckedPacket] = {}

    def slide_window(self):
        while (self.send_base not in self.buffer
               and self.send_base < self.next_seq_num):
            self.send_base += 1


class Receiver:
    def __init__(self, fin_timeout: float):
        self.recv_base = 0
        self.buffer: dict[int, bytes] = {}
        self.receive = True
        self.last_received_time = time.monotonic()
        self.fin_timeout = fin_timeout

    def punch_clock(self):
        self.last_received_time = time.monotonic()

    def check_fin_timeout(self):
        # and len(self.buffer) == 0
        # and self.recv_base > 0
        if (
            time.monotonic() - self.last_received_time > self.fin_timeout
        ):
            self.receive = False


class SelectiveRepeat(TransmissionProtocol):
    def __init__(self, context):
        super().__init__(context, SR_TIMEOUT)
        self.window = WINDOW_SIZE
        self.max_seq_num = 2 * WINDOW_SIZE + 1
        self.stall_timeout = SR_STALL_TIMEOUT

    def _retry_timeouts(self, buffer: dict[int, UnAckedPacket]):
        now = time.monotonic()
        for _, unackd_packet in list(buffer.items()):
            if now - unackd_packet.time > self.timeout:
                logger.debug(RETRY_DATA.format(timeout=self.timeout,
                                               seq_num=unackd_packet.seq_num))
                self.ctx.send_packet(unackd_packet.packet)
                unackd_packet.time = now

    def send_data(self, chunks):
        total_chunks = len(chunks)
        if total_chunks == 0:
            chunks = [b""]
            total_chunks = 1

        sender = Sender()
        last_send_base = 0
        stall_deadline = time.monotonic() + self.stall_timeout

        while sender.send_base < total_chunks:
            while (sender.next_seq_num < sender.send_base + self.window
                   and sender.next_seq_num < total_chunks):
                seq_num = sender.next_seq_num % self.max_seq_num

                packet = encode(TYPE_DATA, seq_num,
                                chunks[sender.next_seq_num])
                logger.debug(SEND_DATA_PACKET.format(seq_num=seq_num))
                self.ctx.send_packet(packet)

                sender.buffer[sender.next_seq_num] = UnAckedPacket(
                    packet,
                    time.monotonic(),
                    seq_num
                )
                sender.next_seq_num += 1

            try:
                ack_packet = self.ctx.get_packet(timeout=SR_ACK_LISTENER_TIMEOUT)
                packet_type, ack_num, _ = decode(ack_packet)
                if packet_type == TYPE_ACK:
                    acked = None
                    for abs_seq_num in list(sender.buffer.keys()):
                        if sender.buffer[abs_seq_num].seq_num == ack_num:
                            acked = abs_seq_num
                            break

                    if acked is None:
                        logger.debug(STALE_ACK.format(seq_num=ack_num))
                    else:
                        sender.buffer.pop(acked)
                        logger.debug(RECV_ACK_DATA.format(seq_num=ack_num))
                        sender.slide_window()

            except TimeoutError:
                pass

            self._retry_timeouts(sender.buffer)

            if sender.send_base != last_send_base:
                stall_deadline = time.monotonic() + self.stall_timeout
                last_send_base = sender.send_base

            if time.monotonic() > stall_deadline:
                logger.error(ERROR_SEND_STALL.format(
                        timeout=self.stall_timeout,
                        confirmed=sender.send_base,
                        total=total_chunks,
                    )
                )
                return False

        return self._send_fin()

    def receive_data(self, chunks):
        receiver = Receiver(IDLE_TIMEOUT)#Receiver(self.timeout * 3)

        while receiver.receive:
            try:
                packet = self.ctx.get_packet(timeout=DATA_LISTENER_TIMEOUT)

                receiver.punch_clock()
                packet_type, seq_num, payload = decode(packet)

                if packet_type == TYPE_FIN:
                    self._recv_fin()
                    return True

                elif packet_type == TYPE_DATA and seq_num is not None:
                    window_idx = receiver.recv_base % self.max_seq_num
                    diff = (seq_num - window_idx) % self.max_seq_num
                    if diff > self.max_seq_num // 2:
                        diff -= self.max_seq_num
                    abs_seq_num = receiver.recv_base + diff

                    ack_packet = encode(TYPE_ACK, seq_num)
                    logger.debug(SEND_ACK_DATA.format(seq_num=seq_num))
                    self.ctx.send_packet(ack_packet)

                    if abs_seq_num < receiver.recv_base:
                        logger.debug(DISCARD_DUP.format(seq_num=seq_num,
                                                        expected=window_idx))

                    elif receiver.recv_base + self.window > abs_seq_num: #receiver.recv_base < abs_seq_num + self.window:
                        receiver.buffer[abs_seq_num] = (b"" if payload is None else payload)
                        delivered = 0
                        while receiver.recv_base in receiver.buffer:
                            chunks.append(
                                receiver.buffer.pop(receiver.recv_base))
                            receiver.recv_base += 1
                            #logger.debug(RECV_DATA.format(seq_num=receiver.recv_base - 1))
                            delivered += 1
                        
                        if delivered:
                            logger.debug(WINDOW_SLIDE.format(delivered=delivered, base=receiver.recv_base, seq=(receiver.recv_base-1) % self.max_seq_num))

                    else:
                        logger.debug(
                            DISCARD_DUP.format(seq_num=seq_num, expected=window_idx))

            except TimeoutError:
                pass
            

            receiver.check_fin_timeout()
        if receiver.recv_base == 0:
            logger.error(NO_DATA_RECEIVED.format(timeout=receiver.fin_timeout))
        else:
            logger.error(
                TRANSFER_INCOMPLETE.format(
                    timeout=receiver.fin_timeout, received=receiver.recv_base
                )
            )
        return False
