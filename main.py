#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# default libraries
import time
import typing as tp
import logging
from queue import Empty
import robonomicsinterface as RI

# modules
from config import read_config
from servers import TCPServer, MyHttpsServer

# global variables
from servers import ROBOT_COMMAND_QUEUE


class MainClass:
    """The main class that initialize servers and launches the loop."""

    def __init__(self) -> None:
        self.config: tp.Dict[str, str] = read_config()
        logging.debug(self.config)

        self.interface = RI.RobonomicsInterface(seed=self.config["robonomics"]["seed"])
        self.current_command: tp.Optional[str] = None

        # starting servers
        self.tcp = TCPServer(
            self.config["tcp_server"]["address"], int(self.config["tcp_server"]["port"])
        )
        self.tcp.start()
        self.http = MyHttpsServer(self.config["eisenkoch"]["address"])
        self.http.start()
        account_data = self.interface.account_info(self.config["eisenkoch"]["address"])
        logging.debug(account_data)
        eisenkoch_balance = round((account_data["data"]["free"] - account_data["data"]["fee_frozen"]) * 10**(-9), 3)
        self.http.set_update_balance(eisenkoch_balance)

    def __get_data(self, block: bool = False) -> tp.Optional[str]:
        try:
            robot_command = ROBOT_COMMAND_QUEUE.get(block)
            logging.debug(f"get command: {robot_command}")
            return robot_command
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
                        self.http.set_status_right("busy")

                    if self.current_command == "left_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("available")

                    if self.current_command == "right_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_right("available")

                    if self.current_command == "send_tokens":
                        try:
                            logging.info(f"get command {self.current_command}")
                            payment = self.config["eisenkoch"]["cost"] * 10**9
                            result = self.interface.send_tokens(self.config["eisenkoch"]["address"], payment)
                            logging.info(result)
                            account_data = self.interface.account_info(self.config["eisenkoch"]["address"])
                            new_balance = round(
                                (account_data["data"]["free"] - account_data["data"]["fee_frozen"]) * 10**(-9), 3)
                            self.http.set_update_balance(new_balance)
                            logging.info("update balance")
                        except Exception as e:
                            logging.error("Not enough balance.")
                            logging.error(e)
                            pass
                        self.http.set_number_waffles(self.http.get_number_waffles() + 1)

                    if self.current_command == "left_timer_start":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("cooking")

                    if self.current_command == "right_timer_start":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_right("cooking")

                    if self.current_command == "left_timer_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_left("finishing")

                    if self.current_command == "right_timer_stop":
                        logging.info(f"get command {self.current_command}")
                        self.http.set_status_right("finishing")

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
