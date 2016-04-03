#!/usr/bin/env python2

import pygame
import thread

from select import select

from socket import *

COLOURS = ['green', 'red', 'blue', 'yellow', 'black', 'white', 'gray', 'cyan', 'magenta', 'lightgray', 'darkgray', 'grey', 'aqua', 'fuchsia', 'lime', 'maroon', 'navy', 'olive', 'purple', 'silver', 'teal']

lock = thread.allocate_lock()
Players = {}
colour_index = 0

def accept_connections(ip, port, q, max_players, UP, DOWN, LEFT, RIGHT, A, B):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(100)
    print 'Listening on port', port
    while True:
        s, a = sock.accept()
        thread.start_new_thread(player_communication, (s, a, q, max_players, UP, DOWN, LEFT, RIGHT, A, B))

def player_communication(sock, addr, q, max_players, UP, DOWN, LEFT, RIGHT, A, B):
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
                    if colour_index < max_players and colour_index >= 0:
                        Players[sock] = colour_index
                        colour_index += 1
                        sock.send('Connected\n')
                        sock.send(COLOURS[Players[sock]] + '\n')
                        q.put('connect')
                    else:
                        sock.send('ERROR\n')
                        print 'Too many players'
                print 'sent to app'

            if 'Up' in msg:
                if UP is not None:
                    pygame.event.post(UP[Players[sock]])
                print 'Up detected from Player', str(Players[sock] + 1)
            if 'Down' in msg:
                if DOWN is not None:
                    pygame.event.post(DOWN[Players[sock]])
                print 'Down detected from Player', str(Players[sock] + 1)
            if 'Right' in msg:
                if RIGHT is not None:
                    pygame.event.post(RIGHT[Players[sock]])
                print 'Right detected from Player', str(Players[sock] + 1)
            if 'Left' in msg:
                if LEFT is not None:
                    pygame.event.post(LEFT[Players[sock]])
                print 'Left detected from Player', str(Players[sock] + 1)
            if 'A' in msg:
                if A is not None:
                    pygame.event.post(A[Players[sock]])
                print 'Shoot detected from Player', str(Players[sock] + 1)
            if 'B' in msg:
                if B is not None:
                    pygame.event.post(B[Players[sock]])
                print 'Reverse detected from Player', str(Players[sock] + 1)
            if 'Ready' in msg:
                q.put('Ready')
            if len(msg) > 0:
                print 'Received', msg, 'from', addr
            else:
                sock.close()
                with lock:
                    del Players[sock]
                    colour_index -= 1
                    print 'Connection from', addr, 'closed!'
                break

