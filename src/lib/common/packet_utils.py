from lib.common.constants import HEADER_SIZE, SEQ_NUMB_SIZE, TYPE_PACKET_SIZE


def encode(pack_type, seq_num=0, payload=b""):
    header = pack_type.to_bytes(TYPE_PACKET_SIZE, "big") + seq_num.to_bytes(
        SEQ_NUMB_SIZE, "big"
    )
    return header + payload


def decode(packet):
    if len(packet) < HEADER_SIZE:
        return None, None, None

    pack_type = int.from_bytes(packet[0:TYPE_PACKET_SIZE], "big")
    seq_num = int.from_bytes(packet[TYPE_PACKET_SIZE:HEADER_SIZE], "big")
    payload = packet[HEADER_SIZE:]
    return pack_type, seq_num, payload
