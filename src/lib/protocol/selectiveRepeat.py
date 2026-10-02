from lib.protocol.transmissionProtocol import TransmissionProtocol
from lib.common.constants import (WINDOW_SIZE, SR_TIMEOUT,
                                  ACK_LISTENER_TIMEOUT, TYPE_DATA, TYPE_ACK,
                                  TYPE_FIN, DATA_LISTENER_TIMEOUT)
from lib.common.packet_utils import encode, decode
from dataclasses import dataclass
import time


@dataclass
class UnAckedPacket():
    packet: bytes
    time: float
    seq_num: int


class Sender():
    def __init__(self):
        self.send_base = 0
        self.next_seq_num = 0
        self.buffer: dict[int, UnAckedPacket] = {}


class Reciever():
    def __init__(self):
        self.recv_base = 0
        self.buffer: dict[int, bytes] = {}
        self.recieve = True


class SelectiveRepeat(TransmissionProtocol):
    def __init__(self, context):
        self.window = WINDOW_SIZE
        self.max_seq_num = 2 * WINDOW_SIZE + 1
        self.timeout = SR_TIMEOUT

        self.ctx = context

    def send_fin(self):
        fin_packet = encode(TYPE_FIN, 0, b"")
        while True:
            self.ctx.send_packet(fin_packet)
            try:
                ack_packet = self.ctx.get_packet(timeout=self.timeout)
                if ack_packet is not None:
                    packet_type, _, _ = decode(ack_packet)
                    if packet_type == TYPE_ACK:
                        break
            except Exception:
                pass

    def send_data(self, chunks):
        total_chunks = len(chunks)
        if total_chunks == 0:
            chunks = [b""]
            total_chunks = 1

        sender = Sender()

        while sender.send_base < total_chunks:
            while ((sender.next_seq_num < sender.send_base + self.window)
                   and (sender.next_seq_num < total_chunks)):
                seq_num = (sender.next_seq_num % self.max_seq_num)

                packet = encode(TYPE_DATA,
                                seq_num,
                                chunks[sender.next_seq_num])
                self.ctx.send_packet(packet)

                sender.buffer[sender.next_seq_num] = UnAckedPacket(
                    packet,
                    time.monotonic(),
                    seq_num)
                sender.next_seq_num += 1

            try:
                ack_packet = self.ctx.get_packet(timeout=ACK_LISTENER_TIMEOUT)
                if ack_packet is not None:
                    packet_type, ack_num, _ = decode(ack_packet)
                    if packet_type == TYPE_ACK:
                        for abs_seq_num in list(sender.buffer.keys()):
                            if sender.buffer[abs_seq_num].seq_num == ack_num:
                                sender.buffer.pop(abs_seq_num)
                                break

            except Exception:
                pass

            now = time.monotonic()
            for abs_seq_num, unackd_packet in list(sender.buffer.items()):
                if now - unackd_packet.time > self.timeout:
                    self.ctx.send_packet(unackd_packet.packet)
                    unackd_packet.time = now

        self.send_fin()

    def recieve_data(self, chunks):
        reciever = Reciever()
        last_received_time = time.monotonic()
        inactivity_timeout = self.timeout * 3

        while reciever.recieve:
            try:
                packet = self.ctx.get_packet(timeout=DATA_LISTENER_TIMEOUT)
                if packet is not None:
                    last_received_time = time.monotonic()
                    packet_type, seq_num, payload = decode(packet)

                    if packet_type == TYPE_FIN:
                        ack_packet = encode(TYPE_ACK, 0, b"")
                        self.ctx.send_packet(ack_packet)
                        reciever.recieve = False

                    elif packet_type == TYPE_DATA and seq_num is not None:
                        window_idx = reciever.recv_base % self.max_seq_num
                        diff = (seq_num - window_idx) % self.max_seq_num
                        if diff > self.max_seq_num // 2:
                            diff -= self.max_seq_num

                        abs_seq_num = reciever.recv_base + diff
                        ack_packet = encode(TYPE_ACK, seq_num, b"")
                        self.ctx.send_packet(ack_packet)

                        if (reciever.recv_base <= abs_seq_num + self.window):
                            reciever.buffer[abs_seq_num] = (b"" if payload is
                                                            None else payload)

                            while reciever.recv_base in reciever.buffer:
                                chunks.append(reciever.buffer.pop(
                                    reciever.recv_base))
                                reciever.recv_base += 1

            except Exception:
                pass

            if (time.monotonic() - last_received_time > inactivity_timeout
                    and len(reciever.buffer) == 0 and reciever.recv_base > 0):
                reciever.recieve = False
