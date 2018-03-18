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
                images_read += 1
                nparr = np.fromstring(image, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                process_image(img_np)
                
        print "Tiempo en procesar todas las imagenes: [{}]".format(time.time()-init_time)
        cv2.destroyAllWindows()
    s.close()

def process_image(image):
    # find the red color game in the image
    upper = np.array([80, 80, 255])
    lower = np.array([0, 0, 180])
    mask = cv2.inRange(image, lower, upper)
    cv2.imshow("Mascara",mask) 


    # find contours in the masked image and keep the largest one
    (_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        # keep the largest one
        c = max(cnts, key=cv2.contourArea)
 
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
 
        # draw a green bounding box surrounding the red game
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
        
        # obtain the centroid
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(image,(cx,cy),2,[0,255,0])

    cv2.imshow("Image", image)
    cv2.waitKey(10)

if __name__ == "__main__":
   main()
