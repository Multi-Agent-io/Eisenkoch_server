#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# default libraries
import time
import typing as tp
import logging
from queue import Empty

# modules
from config import read_config
from servers import TCPServer, MyHttpsServer

# global variables
from servers import ROBOT_COMMAND_QUEUE


class MainClass:
    """The main class that initialize servers and launches the loop."""

    def __init__(self) -> None:
        self.current_command: tp.Optional[str] = None
        self.robot_command: tp.Optional[str] = None

        self.config: tp.Dict[str, str] = read_config()
        logging.debug(self.config)

        # starting servers
        self.tcp = TCPServer(
            self.config["server"]["address"], int(self.config["server"]["port"])
        )
        self.tcp.start()
        self.http = MyHttpsServer()
        self.http.start()

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
                        cooking_time_left = int(self.__get_data(True))
                        self.http.set_left_cooking_time(cooking_time_left)
                        logging.info(f"left cooking time is {cooking_time_left}")

                    if self.current_command == "time_right":
                        logging.info(f"get command {self.current_command}")
                        cooking_time_right = int(self.__get_data(True))
                        self.http.set_right_cooking_time(cooking_time_right)
                        logging.info(f"right cooking time is {cooking_time_right}")

                    if self.current_command == "total_waffles":
                        logging.info(f"get command {self.current_command}")
                        total_waffles = int(self.__get_data(True))
                        self.http.set_number_waffles(total_waffles)
                        logging.info(f"total made waffles is {total_waffles}")

                    if self.current_command == "left_start":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("busy")

                    if self.current_command == "right_start":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("busy")

                    if self.current_command == "left_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("available")

                    if self.current_command == "right_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("available")

                time.sleep(1)
        except KeyboardInterrupt:
            logging.debug("shutting down")
            self.tcp.join()
            self.http.join()
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
