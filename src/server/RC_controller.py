# -*- coding: utf-8-*-

import socket    

ADDRESS = ("192.168.1.38", 2020)

RECTO = "recto\n";
PARO = "paro\n";
DERECHA = "derecha\n";
IZQUIERDA = "izquierda\n";
ATRAS = "atras\n";
ADELANTE = "adelante\n";


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)
    return s

def send_command(s,command):
    s.sendall(command)

def disconnect(s):
    s.close()

if __name__ == "__main__":
    pass
