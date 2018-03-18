# -*- coding: utf-8-*-

from picamera import PiCamera
import time

import io

import socket


IP_PC_JAVI = "192.168.1.42"
PORT = 4400

def send_pict(num_pictures,connection):
    stream = io.BytesIO()
    for i in range(num_pictures):
        yield stream
        
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


def main():
    sock = socket.socket()
    sock.connect((IP_PC_JAVI,PORT))

    connection = sock.makefile("wb") # para que tenga interfaz de "file"
    with PiCamera() as camera:
        camera.rotation = 180
        camera.framerate = 80
        camera.resolution = '640x480'
        camera.start_preview()
        # tiempo de arranque
        time.sleep(2)
        num_fotos = 1000
        time_init = time.time()
        camera.capture_sequence(send_pict(num_fotos,connection),"jpeg",use_video_port=True)
        time_end = time.time()
        print "FPS medio: [{}]".format(num_fotos / (time_end-time_init))
        connection.write("0\n")
        connection.close()


if __name__ == "__main__":
    main()
