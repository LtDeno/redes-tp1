"""Tipos de paquetes - Tipos de mensajes"""
TYPE_START = 1
TYPE_ACK = 2
TYPE_CONFIRM = 3
TYPE_READY = 4
TYPE_DATA = 5
TYPE_ERROR = 6

"""Acciones - Programas"""
ACTION_UPLOAD = "UPLOAD"
ACTION_DOWNLOAD = "DOWNLOAD"
SEPARATOR = "|"

# Tipo de paquete - 1 byte
# Numero de secuencia  - 4 Bytes
TYPE_PACKET_SIZE = 1
SEQ_NUMB_SIZE = 4
HEADER_SIZE = TYPE_PACKET_SIZE + SEQ_NUMB_SIZE


REQUEST_SIZE = 3
PAYLOAD_SIZE = 2900 #A priori, lo podemos cambiar mas adelante.


MAX_RETRIES = 10

"""TIMEOUTS"""
DELAY = 0.5
RECEIVER_TIMEOUT = 4
