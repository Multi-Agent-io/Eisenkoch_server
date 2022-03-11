#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# default libraries
import time
import typing as tp
import logging
from queue import Empty

# modules
from config import read_config
from servers import TCPServer

# global variables
from servers import ROBOT_COMMAND_QUEUE


class MainClass:
    """The main class that initialize servers and launches the loop."""

    def __init__(self) -> None:
        self.current_command: tp.Optional[str] = None
        self.robot_command: tp.Optional[str] = None

        # waffles variables
        self.cooking_time_left: int = 0

        self.config: tp.Dict[str, str] = read_config()
        logging.debug(self.config)

        # available servers
        self.servers: list = self.__start_servers()

    def __start_servers(self) -> list:
        self.s: list = []
        self.tcp = TCPServer(
            self.config["server"]["address"], int(self.config["server"]["port"])
        )
        self.tcp.start()
        self.s.append(self.tcp)
        return self.s

    def __get_data(self, block: bool = False) -> tp.Optional[str]:
        try:
            self.robot_command = ROBOT_COMMAND_QUEUE.get(block)
            logging.info(f"get command: {self.robot_command}")
            return self.robot_command
        except Empty:
            logging.debug("the queue is empty")
            return None

    def spin(self) -> None:
        try:
            while True:
                self.current_command = self.__get_data()
                if self.current_command:
                    if self.current_command == "time_left":
                        logging.info("get command 'time_left'")
                        self.cooking_time_left = int(self.__get_data(True))
                        logging.info(f"time is {self.cooking_time_left}")
                    if self.current_command == "left_start":
                        self.cooking_left(self.cooking_time_left)

                time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("shutting down")
            exit()
            
    @staticmethod
    def cooking_left(cooking_time: int):
        logging.info("start cooking left waffle")
        while cooking_time != 0:
            logging.info(f"current time is {cooking_time}")
            cooking_time = cooking_time - 1
            time.sleep(1)
        logging.info("waffles ready")


if __name__ == "__main__":
    MainClass().spin()
