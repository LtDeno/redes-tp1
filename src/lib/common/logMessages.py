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
    "[{addr}] - Iniciando accion de {action} del archivo {filename} con {protocol}"
)

"""Logins de fileHandler"""
ERROR_EMPTY_LIST = (
    "No se pudo guardar el archivo {file_path}, la lista de bytes esta vacia"
)
CREATE_FILE = "Creando el archivo '{filename}' en el directorio '{base_path}'."
ERROR_PROCESS_FILE = "Error de E/S al procesar el archivo {filename}"
FILE_NOT_FOUND = "Archivo no encontrado en la ruta establecida: {file_path}"

"""Logins downloadhandler"""
ERROR_READ_FILE = "[{addr}] -- Error al leer el archivo '{filename}'."
SENDING_FILE = "[{addr}] -- Enviando archivo '{filename}'..."
SENT_FILE = "[{addr}] -- Archivo '{filename}' enviado."

"""Logins uploadhandler"""
RECEIVING_FILE = "[{addr}] -- Recibiendo el archivo '{filename}'..."
SAVE_FILE = "[{addr}] -- Archivo '{filename}' guardado."
