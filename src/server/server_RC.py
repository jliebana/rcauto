# -*- coding: utf-8-*-

import socket
import os
import cv2
import numpy as np

import time

def main():
     
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 4400 # 
 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket creado'
 
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
     
    print 'Socket bind completado'
 
    #Start listening on socket
    s.listen(10)
    print 'Socket escuchando'
 
    images_read = 0
    path = "/home/javier/cocheRC/imagenes"
    
    if not os.path.exists(path):
        os.makedirs(path)

    #now keep talking with the client
    while True:
        #wait to accept a connection - blocking call
        connection, addr = s.accept()
        print 'Conectado con ' + addr[0] + ':' + str(addr[1])
        connection = connection.makefile('rb')
        num_bytes = -1
        init_time = time.time()
        while num_bytes != 0:
            line = connection.readline()
            num_bytes = long(line.strip())
            if num_bytes > 0 :
                image = connection.read(num_bytes)
                print "Imagen leida. Tamaño [{}]".format(len(image))
                #with open(os.path.join(path,str(images_read)+".jpeg"),"w") as f:
                #    f.write(image)
                images_read += 1
                nparr = np.fromstring(image, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow("Imagen de la Raspberry",img_np)
                cv2.waitKey(15)
                
        print "Tiempo en procesar todas las imagenes: [{}]".format(time.time()-init_time)
        cv2.destroyAllWindows()
    s.close()

if __name__ == "__main__":
   main()
