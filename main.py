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
        self.cooking_time_right: int = 0
        self.total_waffles: int = 0

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
            logging.debug(f"get command: {self.robot_command}")
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
                        logging.info(f"get command {self.current_command}")
                        self.cooking_time_left = int(self.__get_data(True))
                        logging.info(f"left cooking time is {self.cooking_time_left}")
                    if self.current_command == "time_right":
                        logging.info(f"get command {self.current_command}")
                        self.cooking_time_right = int(self.__get_data(True))
                        logging.info(f"right cooking time is {self.cooking_time_right}")
                    if self.current_command == "total_waffles":
                        logging.info(f"get command {self.current_command}")
                        self.total_waffles = int(self.__get_data(True))
                        logging.info(f"total made waffles is {self.total_waffles}")

                    if self.current_command == "left_start":
                        logging.info(f"get command {self.current_command}")
                        self.cooking_timer(self.cooking_time_left)
                    if self.current_command == "right_start":
                        logging.info(f"get command {self.current_command}")
                        self.cooking_timer(self.cooking_time_right)

                time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("shutting down")
            exit()
            
    @staticmethod
    def cooking_timer(cooking_time: int):
        logging.info("start cooking waffle")
        while cooking_time != 0:
            logging.info(f"current time is {cooking_time}")
            cooking_time = cooking_time - 1
            time.sleep(1)
        logging.info("waffles ready")


if __name__ == "__main__":
    MainClass().spin()
