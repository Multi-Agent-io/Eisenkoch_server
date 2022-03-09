#!/usr/bin/env python3
import time
import socket
import select
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)

TIME_LEFT = 0


def cooking_left(cooking_time: int):
    logging.info("start cooking left waffle")
    while cooking_time != 0:
        logging.info(f"current time is {cooking_time}")
        cooking_time = cooking_time - 1
        time.sleep(1)
    logging.info("waffles ready")


def readline(s):
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


try:
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ("192.168.57.1", 50001)
    logging.info("starting up on %s port %s" % server_address)
    server.bind(server_address)
except Exception as e:
    logging.error(f"Can't create the server. Get error:{e}")
    exit()

# Listen for incoming connections
server.listen(3)

# set three lists containing communication channels to monitor.

inputs = [server]
outputs = [server]
exceptions = [server]


try:
    # The main portion of the server program loops, calling select() to block and wait for network activity.
    while inputs:

        # Wait for at least one of the sockets to be ready for processing
        logging.debug("waiting for the next event")
        readable, writable, exceptional = select.select(inputs, outputs, exceptions)

        # Handle inputs
        for cur_socket in readable:
            if cur_socket is server:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = cur_socket.accept()
                logging.debug(f"new connection from {client_address}")
                inputs.append(connection)
                outputs.append(connection)
                exceptions.append(connection)

            # The next case is an established connection with a client that has sent data.
            else:
                command = readline(cur_socket)
                if len(command) != 0:
                    logging.info(command + '\n')
                if command == "GET main":
                    cur_socket.send("main 1".encode())
                    logging.info("done")
                if command == "time_left":
                    logging.info("inside time_left")
                    TIME_LEFT = int((readline(cur_socket)))
                    logging.info(f"time is {TIME_LEFT}")
                if command == "left_start":
                    cooking_left(TIME_LEFT)

        # Handle "exceptional conditions"
        for cur_except_socket in exceptional:
            logging.error(f"handling exceptional condition for {cur_except_socket.getpeername()}")
            # Stop listening for input on the connection
            inputs.remove(cur_except_socket)
            if cur_except_socket in outputs:
                outputs.remove(cur_except_socket)
            if cur_except_socket in exceptions:
                exceptions.remove(cur_except_socket)
            cur_except_socket.close()

except KeyboardInterrupt:
    exit()

except Exception as e:
    logging.info(f"global error {e}")
    exit()
