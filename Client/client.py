import socket
import threading

nombre = input("Ingrese su nombre:")

host = '127.0.0.1'
port = 55000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def recibirMensaje():
    while True:
        try:
            mensaje = client.recv(1024).decode('utf-8')
            client.send(nombre.encode('utf-8')) if mensaje == "#nombre" else print(mensaje)
        except:
            print("Ocurrio un error")
            client.close()
            break


def escribirMensaje():
    while True:
        mensaje = f"{nombre} : {input('')}"
        client.send(mensaje.encode('utf-8'))


hiloRecibir = threading.Thread(target=recibirMensaje)
hiloRecibir.start()

hiloEscribir = threading.Thread(target=escribirMensaje)
hiloEscribir.start()
