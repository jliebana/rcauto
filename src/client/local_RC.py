# -*- coding: utf-8-*-

from picamera import PiCamera
import time

import io


def main():
    #Prueba para medir lo que se tarda en hacer una captura
    with PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = "640x480"
        camera.start_preview()
        # tiempo de arranque
        time.sleep(2)
        num_fotos = 0
        stream = io.BytesIO()
        last = time.time()
        initial = time.time()
        for _ in camera.capture_continuous(stream,"jpeg",use_video_port=True):
            #print "Tiempo en obtener una foto [{}]".format(time.time()-last)
            #last = time.time()
            if num_fotos == 1000:
                break
            num_fotos+=1
            #size = stream.tell()
            #print "Tamaño de la imagen: [{}]".format(size)
            #stream.seek(0)

            #limpiamos el stream
            stream.seek(0)
            stream.truncate()
        print "Tiempo total en tomar todas las fotos [{}]".format(time.time()-initial)



if __name__ == "__main__":
    main()
