"""Logins de server.py"""

SERVER_LISTENING = "Servidor escuchando en {host}:{port}"
NEW_CLIENT = "Nuevo cliente conectado: {addr}"
CLIENT_REMOVED = "Cliente {addr} eliminado"
SERVER_SHUTDOWN = "--- Servidor Cerrado ---"

"""Logins de clientHandler"""
ERROR_CLIENTHANDLER = "[{addr}] - ERROR: {err}"
ERROR_FORMAT_REQUEST = "[{addr}] - Error formato de peticion invalido"
ERROR_UNKNOWN_ACTION = "[{addr}] Acción desconocida: {action}"
EXECUTE_ACTION = (
    "[{addr}] - Iniciando accion de {action} del archivo {filename}"
    "con {protocol}"
)

"""Logins downloadhandler"""
ERROR_READ_FILE = "[{addr}] -- Error al leer el archivo '{filename}'."
SENDING_FILE = "[{addr}] -- Enviando archivo '{filename}'..."
SENT_FILE = "[{addr}] -- Archivo '{filename}' enviado."

"""Logins uploadhandler"""
RECEIVING_FILE = "[{addr}] -- Recibiendo el archivo '{filename}'..."
SAVE_FILE = "[{addr}] -- Archivo '{filename}' guardado."
