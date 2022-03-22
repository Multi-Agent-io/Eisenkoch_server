#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from typing import Dict, Optional, Union

# fast api imports
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


class MyHttpsServer(Thread):
    def __init__(self, address: str) -> None:

        # create thread and add main variables
        Thread.__init__(self)
        self.account_address: str = address
        self.address_balance: int = 0
        self.number_of_waffles: Optional[int] = None
        self.cooking_time_left: int = 0
        self.cooking_time_right: int = 0
        self.status_left: str = "available"
        self.status_right: str = "available"

        # FastAPI object
        self.app = FastAPI()

        # add middleware
        origins = ["*"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get("/")
        async def root() -> Dict[str, str]:
            return {"message": "Hello World"}

        @self.app.get("/robot-address")
        async def robot_address() -> Dict[str, str]:
            return {"message": self.account_address}

        @self.app.get("/total-waffles", response_class=JSONResponse)
        def waffles_numbers() -> Dict[str, str]:
            if self.number_of_waffles is not None:
                return {"status": str(self.number_of_waffles)}
            else:
                return {"status": "waiting"}

        @self.app.get("/cooking-time-left", response_class=JSONResponse)
        def left_cooking() -> Dict[str, Union[str, int]]:
            if self.cooking_time_left != 0:
                return {"status": self.cooking_time_left}
            else:
                return {"status": "waiting"}

        @self.app.get("/cooking-time-right", response_class=JSONResponse)
        def right_cooking() -> Dict[str, Union[str, int]]:
            if self.cooking_time_right != 0:
                return {"status": self.cooking_time_right}
            else:
                return {"status": "waiting"}

        @self.app.get("/status-left")
        async def status_left() -> Dict[str, str]:
            return {"message": self.status_left}

        @self.app.get("/status-right")
        async def status_right() -> Dict[str, str]:
            return {"message": self.status_right}

        @self.app.get("/update-balance")
        async def update_balance() -> Dict[str, int]:
            return {"message": self.address_balance}

    def run(self) -> None:
        uvicorn.run(self.app, host="127.0.0.1", port=5000, log_level="debug")

    def set_number_waffles(self, number: int) -> None:
        self.number_of_waffles = number

    def set_right_cooking_time(self, time: int) -> None:
        self.cooking_time_right = time

    def set_left_cooking_time(self, time: int) -> None:
        self.cooking_time_left = time

    def set_status_left(self, status: str) -> None:
        self.status_left = status

    def set_status_right(self, status: str) -> None:
        self.status_right = status

    def set_update_balance(self, balance: int):
        self.address_balance = balance


if __name__ == "__main__":
    MyHttpsServer("4F3b1hoyFW1N4V9H7ggUq23MjXyK8C62s5v6469k9qEBktDf").start()
