import socket
import threading

host = '127.0.0.1'
port = 55000

"""
    Definimos que socket vamos a usar:
        AF_INET nos permite trabajar con el host y port
        SOCK_STREAM nos permite trabajar con el protocolo TCP
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

""" Pasamos los datos de la conexion en una tupla
 y dejamos el socket en escucha """
server.bind((host, port))
server.listen()
print(f"Server corriendo {host}:{port}")

usuarios = []
conexionesUsuarios = []

"""
    cuando un usuario envie un mensaje esta funcion se encarga de transmitirlo a los demas usuarios
"""


def transmitirMensaje(mensaje, usuarioEmisor):
    for usuarioReceptor in conexionesUsuarios:
        if usuarioReceptor != usuarioEmisor:
            usuarioReceptor.send(mensaje)


"""
    Para manejar los mensajes de los usuarios
    toma como parametro el usuario que envio el mensaje
"""


def handleMessage(usuarioEmisor):
    while True:  # para que este en escucha siempre
        try:
            mensaje = usuarioEmisor.recv(1024)  # peso maximo del mensaje
            transmitirMensaje(mensaje, usuarioEmisor)
        except:
            """
                si hay algun problema con el usuario que envio el mensaje hay que 
                identificar cual es, como se agregar en paralelo podemos obtenerlo 
                con la misma posicion de la lista de conexiones
                luego se eliminan y se cierra la conexion
            """
            usuario = usuarios[conexionesUsuarios.index(usuarioEmisor)]
            transmitirMensaje(f"ChatAPP: {usuario} desconectado".encode('utf-8'), usuarioEmisor)
            conexionesUsuarios.remove(usuarioEmisor)
            usuarios.remove(usuario)
            usuarioEmisor.close()
            break


# para aceptar y manejar las conexiones
def recibirConexiones():
    while True:
        # acepta a quien se conecta en a host:port, recibe la conexion su direccion
        conexion, direccion = server.accept()
        conexion.send("#nombre".encode('utf-8'))  # enviamos un mensaje a la app del usuario
        usuario = conexion.recv(1024).decode('utf-8')

        conexionesUsuarios.append(conexion)
        usuarios.append(usuario)

        print(f"{usuario} conectado con {str(direccion)}")

        mensajeInformativo = f"ChatAPP : {usuario} ha ingresado al chat".encode('utf-8')
        transmitirMensaje(mensajeInformativo, conexion)
        conexion.send("Conexion con el servidor exitosa".encode('utf-8'))

        # Necesitamos que cada usuario tenga un hilo dedicado para el manejo de mensajes
        hilo = threading.Thread(target=handleMessage, args=(conexion,))
        hilo.start()


recibirConexiones()
