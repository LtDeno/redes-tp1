from lib.common.constants import SEPARATOR


def build_request(action, filename, protocol):
    return f"{action}{SEPARATOR}{filename}{SEPARATOR}{protocol}".encode()


def parse_request(payload):
    parts_request = payload.decode().split(SEPARATOR)
    return parts_request  # action, filename, protocol
