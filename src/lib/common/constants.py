"""Tipos de paquetes - Tipos de mensajes"""

TYPE_START = 1
TYPE_ACK = 2
TYPE_CONFIRM = 3
TYPE_READY = 4
TYPE_DATA = 5
TYPE_ERROR = 6
TYPE_FIN = 7

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
PAYLOAD_SIZE = 2900  # A priori, lo podemos cambiar mas adelante.

HANDSHAKE_RETRIES = 10  

MAX_RETRIES = 10

READY_BURST = 3        # cantidad de READY
READY_DELAY = 0.05    
CONFIRM_TIMEOUT = 1.0  # reintento de CONFIRM en el cliente
READY_WINDOW = 5.0     # ventana total del cliente para recibir READY (s)

"""TIMEOUTS"""
DELAY = 0.5
QUEUE_TIMEOUT = 10
RECEIVER_TIMEOUT = 4


""" Selective Repeat """

WINDOW_SIZE = 8
SR_TIMEOUT = 0.52  # un poco mayor a 40ms, que es el RTT por consigna
ACK_LISTENER_TIMEOUT = 0.05
DATA_LISTENER_TIMEOUT = 0.10
