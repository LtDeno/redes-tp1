# TP1 de Redes

## Cómo ejecutar la aplicación
### Servidor
> start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
Donde:
* -h (--help) muestra el uso del comando;
* -v (--verbose) y -q (--quiet) son para aumentar y dismunuir la verbosidad, respectivamente;
* -H (--host) es para especificar la direción de red para el host del servidor;
* -p (--port) es para especificar el puerto en la direción de red donde el servidor escuchará por clientes entrantes;
* -s (--storage) es para especificar el path dentro del servidor donde se almacenarán los archivos subidos, y de donde se descargarán.

### Cliente para subida
> upload [-h] [-v | -q] [-H ADDR] [-p PORT] [-s FILEPATH] [-n FILENAME] [-r protocol]
Donde:
* -h (--help) muestra el uso del comando;
* -v (--verbose) y -q (--quiet) son para aumentar y dismunuir la verbosidad, respectivamente;
* -H (--host) es para especificar la direción de red para el host del servidor;
* -p (--port) es para especificar el puerto en la direción de red donde el servidor está escuchando por clientes;
* -s (--src) es para especificar el path donde se encuentra el archivo a subir;
* -n (--name) es para especificar el nombre del archivo a subir;
* -r (--protocol) es para especificar el protocolo de subida, puede ser Stop and Wait (sw) o Selective Repeat (sr).

### Cliente para bajada
> download [-h] [-v | -q] [-H ADDR] [-p PORT] [-d FILEPATH] [-n FILENAME] [-r protocol]
Donde:
* -h (--help) muestra el uso del comando;
* -v (--verbose) y -q (--quiet) son para aumentar y dismunuir la verbosidad, respectivamente;
* -H (--host) es para especificar la direción de red para el host del servidor;
* -p (--port) es para especificar el puerto en la direción de red donde el servidor está escuchando por clientes;
* -d (--dst) es para especificar el path donde se almacenará el archivo a bajar;
* -n (--name) es para especificar el nombre que se desea bajar;
* -r (--protocol) es para especificar el protocolo de bajada, puede ser Stop and Wait (sw) o Selective Repeat (sr).

### Midiendo tiempos (client-side)
> time [cmd]

## Integrantes
Camila Kotelchuk - 110289
Lorenzo Kwiatkowski - 110239
Lautaro de Nobili - 107394
