# Eisenkoch server

This program implements connection between RPI4 and UR3 robot via tcp client-server architecture. 
RPI and robot must be in one network.
Other part of project start http server and provide status information about robot.

## Requirements
To start the program you should install docker. Link how to download and install you can find [here](https://docs.docker.com/engine/install/ubuntu/).

## Installation

First you need to download repository:
```shell
git clone https://github.com/Multi-Agent-io/Eisenkoch_server.git
```
Go into the repository to ***config*** subdirectory and rename and fill in config file:
```shell
cd Eisenkoch_server
mv config_template.yaml config.yaml 
nano config.yaml
```
All information about address and port inside config file.

Next step is a build docker image. Go back to main directory and start the script:
```shell
cd ..
bash docker/install_docker.sh
```
Wait for the installation to finish.

## Start

To start program run next:
```shell
bash docker/run_docker.sh
```