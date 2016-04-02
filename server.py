#!/usr/bin/env python2

import pygame
import thread

from select import select

from socket import *

PORT = 12345
IP = ''
SERVER = (IP, PORT)


lock = thread.allocate_lock()
Players = {}
colours = ['Yellow', 'Blue', 'Red', 'Green']
colour_index = 0

LEFT = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_g),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_j)
        ]

RIGHT = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_k)
        ]

SHOOT = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m)
        ]

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
    global colour_index
    print 'Client connected from', addr
    while True:
        read_socks, _, _ = select([sock], [], [])
        if len(read_socks) > 0:
            msg = sock.recv(1024)
            print msg
            if 'connect' in msg:
                print 'recv from app'
                with lock:
                    if colour_index < 4 and colour_index >= 0:
                        Players[sock] = colour_index
                        colour_index += 1
                        sock.send('Connected\n')
#                        sock.send(colours[Players[sock]] + '\n')
                    else:
                        sock.send('ERROR\n')
                        print 'Too many players'
                print 'sent to app'
            if 'Right' in msg:
#                pygame.event.post(RIGHT[Players[sock]])
                print 'Right detected from Player', str(Players[sock] + 1)
            if 'Left' in msg:
#                pygame.event.post(LEFT[Players[sock]])
                print 'Left detected from Player', str(Players[sock] + 1)
            if 'Shoot' in msg:
#                pygame.event.post(SHOOT[Players[sock]])
                print 'Shoot detected from Player', str(Players[sock] + 1)
            if len(msg) > 0:
                print 'Received', msg, 'from', addr
            else:
                sock.close()
                with lock:
                    del Players[sock]
                    colour_index -= 1
                    print 'Connection from', addr, 'closed!'
                break

if __name__ == '__main__':
    accept_connections()

