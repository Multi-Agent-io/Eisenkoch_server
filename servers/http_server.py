#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from typing import Dict, Optional, Union

# fast api imports
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse


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

        self.app.mount("/dist", StaticFiles(directory="dist"), name="dist")
        self.app.mount("/css", StaticFiles(directory="dist/css"), name="css")
        self.app.mount("/js", StaticFiles(directory="dist/js"), name="js")
        self.app.mount("/img", StaticFiles(directory="dist/img"), name="img")
        self.app.mount("/media", StaticFiles(directory="dist/media"), name="media")

        self.templates = Jinja2Templates(directory="dist")

        @self.app.get("/", response_class=HTMLResponse)
        async def root(request: Request) -> Dict[str, str]:
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.get("/total-waffles", response_class=JSONResponse)
        def waffles_numbers() -> Dict[str, str]:
            if self.number_of_waffles is not None:
                return {"status": str(self.number_of_waffles)}
            else:
                return {"status": "waiting"}

        @self.app.get("/status-left", response_class=JSONResponse)
        async def status_left() -> Dict[str, str]:
            return {"status": self.status_left, "baking_duration": self.cooking_time_left}

        @self.app.get("/status-right", response_class=JSONResponse)
        async def status_right() -> Dict[str, str]:
            return {"status": self.status_right, "baking_duration": self.cooking_time_right}

        @self.app.get("/update-balance", response_class=JSONResponse)
        async def update_balance() -> Dict[str, int]:
            return {"balance": str(self.address_balance)}

    def run(self) -> None:
        uvicorn.run(self.app, host="127.0.0.1", port=5000, log_level="debug")

    def set_number_waffles(self, number: int) -> None:
        self.number_of_waffles = number

    def get_number_waffles(self) -> int:
        return self.number_of_waffles

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
    MyHttpsServer("4CFXBSbwrdjAsAXtQ8Ck9Uiq8qSeKkjNjtnXjnUKJSAhDpcM").start()
