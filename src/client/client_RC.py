# -*- coding: utf-8-*-

from picamera import PiCamera
import time

import io

import socket


IP_PC_JAVI = "192.168.1.42"
PORT = 4400

def main():
    sock = socket.socket()
    sock.connect((IP_PC_JAVI,PORT))

    connection = sock.makefile("wb") # para que tenga interfaz de "file"
    with PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = '640x320'
        camera.start_preview()
        # tiempo de arranque
        time.sleep(2)
        num_fotos = 3000
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream,"jpeg"):
            if num_fotos < 1:
                break
            num_fotos-=1
            size = stream.tell()
            print "Mandando imagen de tamaño: [{}]".format(size)
            connection.write((str(size)+"\n").encode())
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            connection.flush()

            #limpiamos el stream
            stream.seek(0)
            stream.truncate()

        connection.write("0\n")
        connection.close()


if __name__ == "__main__":
    main()
