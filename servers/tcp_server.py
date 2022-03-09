#!/usr/bin/env python3
import time
import select
import socket
import logging
from threading import Thread

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)


class TCPServer(Thread):

    def __init__(self, address: str, port: int):
        Thread.__init__(self)
        self.cur_except_socket = None
        self.cur_socket = None
        self.address: str = address
        self.port: int = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.address, self.port)
        logging.info("starting up on %s port %s" % self.server_address)
        self.server.bind(self.server_address)

        # waffles variables
        self.cooking_time_left: int

        # set three lists containing communication channels to monitor.
        self.inputs: list = [self.server]
        self.outputs: list = [self.server]
        self.exceptions: list = [self.server]

    def run(self) -> None:

        # Listen for incoming connections
        self.server.listen(3)
        try:
            # The main portion of the server program loops, calling select() to block and wait for network activity.
            while self.inputs:

                # Wait for at least one of the sockets to be ready for processing
                logging.debug("waiting for the next event")
                self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs,
                                                                               self.exceptions)

                # Handle inputs
                for self.cur_socket in self.readable:
                    if self.cur_socket is self.server:
                        # A "readable" server socket is ready to accept a connection
                        self.connection, self.client_address = self.cur_socket.accept()
                        logging.debug(f"new connection from {self.client_address}")
                        self.inputs.append(self.connection)
                        self.outputs.append(self.connection)
                        self.exceptions.append(self.connection)

                    # The next case is an established connection with a client that has sent data.
                    else:
                        self.command = self.__readline(self.cur_socket)
                        if len(self.command) != 0:
                            logging.info(self.command + '\n')
                        if self.command == "GET main":
                            self.cur_socket.send("main 1".encode())
                            logging.info("done")
                        if self.command == "time_left":
                            logging.info("inside time_left")
                            self.cooking_time_left = int((self.__readline(self.cur_socket)))
                            logging.info(f"time is {self.cooking_time_left}")
                        if self.command == "left_start":
                            self.cooking_left(self.cooking_time_left)

                # Handle "exceptional conditions"
                for self.cur_except_socket in self.exceptional:
                    logging.error(f"handling exceptional condition for {self.cur_except_socket.getpeername()}")
                    # Stop listening for input on the connection
                    self.inputs.remove(self.cur_except_socket)
                    if self.cur_except_socket in self.outputs:
                        self.outputs.remove(self.cur_except_socket)
                    if self.cur_except_socket in self.exceptions:
                        self.exceptions.remove(self.cur_except_socket)
                    self.cur_except_socket.close()

        except KeyboardInterrupt:
            exit()

        except Exception as e:
            logging.info(f"global error {e}")
            exit()

    @staticmethod
    def __readline(s):
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
        return res.decode('ascii')[:-1]

    @staticmethod
    def cooking_left(cooking_time: int):
        logging.info("start cooking left waffle")
        while cooking_time != 0:
            logging.info(f"current time is {cooking_time}")
            cooking_time = cooking_time - 1
            time.sleep(1)
        logging.info("waffles ready")


if __name__ == "__main__":
    tcp_server = TCPServer("192.168.57.1", 50001)
    tcp_server.start()
