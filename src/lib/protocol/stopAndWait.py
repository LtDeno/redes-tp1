from lib.protocol.transmissionProtocol import TransmissionProtocol
from lib.common.constants import (SW_TIMEOUT, ACK_LISTENER_TIMEOUT, TYPE_DATA,
                                  TYPE_ACK, TYPE_FIN, DATA_LISTENER_TIMEOUT)
from lib.common.packet_utils import encode, decode
import time


class Sender():
    def __init__(self):
        self.seq_num = 0
        self.abs_seq_num = 0


class Receiver():
    def __init__(self, fin_timeout: float):
        self.expected_seq_num = 0
        self.receive = True
        self.last_received_time = time.monotonic()
        self.fin_timeout = fin_timeout

    def punch_clock(self):
        self.last_received_time = time.monotonic()

    def check_fin_timeout(self):
        if (time.monotonic() - self.last_received_time > self.fin_timeout
                and self.expected_seq_num > 0):
            self.receive = False


class StopAndWait(TransmissionProtocol):
    def __init__(self, context):
        self.timeout = SW_TIMEOUT
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

        while sender.abs_seq_num < total_chunks:
            wrapped_seq_num = sender.seq_num % 2
            packet = encode(TYPE_DATA,
                            wrapped_seq_num,
                            chunks[sender.abs_seq_num])

            packet_acknowledged = False
            while not packet_acknowledged:
                self.ctx.send_packet(packet)
                start_time = time.monotonic()

                while time.monotonic() - start_time < self.timeout:
                    try:
                        ack_packet = self.ctx.get_packet(
                            timeout=ACK_LISTENER_TIMEOUT)
                        if ack_packet is not None:
                            packet_type, ack_num, _ = decode(ack_packet)
                            if (packet_type == TYPE_ACK
                                    and ack_num == wrapped_seq_num):
                                packet_acknowledged = True
                                break
                    except Exception:
                        pass

                if packet_acknowledged:
                    break

            sender.abs_seq_num += 1
            sender.seq_num += 1

        self.send_fin()

    def receive_data(self, chunks):
        receiver = Receiver(self.timeout * 3)

        while receiver.receive:
            try:
                packet = self.ctx.get_packet(timeout=DATA_LISTENER_TIMEOUT)
                if packet is not None:
                    receiver.punch_clock()
                    packet_type, seq_num, payload = decode(packet)

                    if packet_type == TYPE_FIN:
                        ack_packet = encode(TYPE_ACK, 0, b"")
                        self.ctx.send_packet(ack_packet)
                        receiver.receive = False
                        break

                    elif packet_type == TYPE_DATA and seq_num is not None:
                        wrapped_seq_num = receiver.expected_seq_num % 2

                        ack_packet = encode(TYPE_ACK, seq_num, b"")
                        self.ctx.send_packet(ack_packet)

                        if seq_num == wrapped_seq_num:
                            chunks.append(b"" if payload is None else payload)
                            receiver.expected_seq_num += 1

            except Exception:
                pass

            receiver.check_fin_timeout()
