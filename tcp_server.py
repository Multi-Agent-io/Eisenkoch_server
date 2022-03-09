#!/usr/bin/env python3
import time
import socket
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
    try:
        res = b""
        while 1:
            c = s.recv(1)
            if len(c) == 0:
                break
            res += c
            #logging.info(c)
            if c == b"\n":
                break
        return res.decode('ascii')[:-1]
    except Exception:
        return ""


try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ("192.168.57.1", 50001)
    logging.info("starting up on %s port %s" % server_address)
    sock.bind(server_address)
except Exception as e:
    logging.error(f"Can't create the server. Get error:{e}")
    exit()

# Listen for incoming connections
sock.listen(3)


try:
    logging.info("waiting for a connection")
    connection, client_address = sock.accept()
    logging.info("successful connect")
    while True:
        for e in range(10):
            # Wait for a connection
            command = readline(connection)
            logging.info(command + '\n')
            if command == "GET main":
                connection.send("main 1".encode())
                logging.info("done")
            if command == "time_left":
                logging.info("inside time_left")
                TIME_LEFT = int((readline(connection)))
                logging.info(f"time is {TIME_LEFT}")
            if command == "left_start":
                cooking_left(TIME_LEFT)


except KeyboardInterrupt:
    exit()

except Exception:
    logging.info("global error")
    exit()
