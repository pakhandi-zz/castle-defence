#!/usr/bin/env python

import thread

from select import select

from socket import *

PORT = 12345
IP = ''
SERVER = (IP, PORT)

def accept_connections():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(SERVER)
    sock.listen(100)
    print 'Listening on port', PORT
    while True:
        client = sock.accept()
        thread.start_new_thread(player_communication, client)

def player_communication(sock, addr):
    print 'Client connected from', addr
    while True:
        read_socks, _, _ = select([sock], [], [])
        if len(read_socks) > 0:
            msg = sock.recv(1024)
            if len(msg) > 0:
                print 'Received', msg, 'from', addr
            else:
                sock.close()
                print 'Connection from', addr, 'closed!'
                break

if __name__ == '__main__':
    accept_connections()

