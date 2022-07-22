#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import select
import socket
import logging
from threading import Thread
from queue import SimpleQueue
import typing as tp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

ROBOT_COMMAND_QUEUE: SimpleQueue = SimpleQueue()


class TCPServer(Thread):
    def __init__(self, address: str, port: int) -> None:
        Thread.__init__(self)

        # additional variables

        self.readable: tp.Optional[tp.List[tp.Any]] = None
        self.writable: tp.Optional[tp.List[tp.Any]] = None
        self.exceptional: tp.Optional[tp.List[tp.Any]] = None
        self.command: tp.Optional[str] = None

        self.address: str = address
        self.port: int = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.address, self.port)
        logging.info("starting up on %s port %s" % self.server_address)
        self.server.bind(self.server_address)

        # set three lists containing communication channels to monitor.
        self.inputs: list = [self.server]
        self.outputs: list = [self.server]
        self.exceptions: list = [self.server]

    def run(self) -> None:
        global ROBOT_COMMAND_QUEUE
        # Listen for incoming connections
        self.server.listen(3)
        try:
            # The main portion of the server program loops, calling select() to block and wait for network activity.
            while self.inputs:

                # Wait for at least one of the sockets to be ready for processing
                logging.debug("waiting for the next event")
                self.readable, self.writable, self.exceptional = select.select(
                    self.inputs, self.outputs, self.exceptions
                )

                # Handle inputs
                for cur_socket in self.readable:
                    if cur_socket is self.server:
                        # A "readable" server socket is ready to accept a connection
                        connection, client_address = cur_socket.accept()
                        logging.info(f"new connection from {client_address}")
                        self.inputs.append(connection)
                        self.outputs.append(connection)
                        self.exceptions.append(connection)

                    # The next case is an established connection with a client that has sent data.
                    else:
                        self.command = self.__readline(cur_socket)
                        if len(self.command) != 0:
                            logging.debug(self.command + "\n")
                            ROBOT_COMMAND_QUEUE.put_nowait(self.command)

                # Handle "exceptional conditions"
                for cur_except_socket in self.exceptional:
                    logging.error(
                        f"handling exceptional condition for {cur_except_socket.getpeername()}"
                    )
                    # Stop listening for input on the connection
                    self.inputs.remove(cur_except_socket)
                    if cur_except_socket in self.outputs:
                        self.outputs.remove(cur_except_socket)
                    if cur_except_socket in self.exceptions:
                        self.exceptions.remove(cur_except_socket)
                    cur_except_socket.close()

        except KeyboardInterrupt:
            exit()

        except Exception as e:
            logging.info(f"global error {e}")
            exit()

    @staticmethod
    def __readline(s) -> str:
        """
        function get bytes buffer and return string
        :param s: socket connection
        :return: string
        """
        res = b""
        while 1:
            c = s.recv(1)
            if len(c) == 0:
                break
            res += c
            if c == b"\n":
                break
        return res.decode("ascii")[:-1]


if __name__ == "__main__":
    tcp_server = TCPServer("192.168.57.1", 50001)
    tcp_server.start()
