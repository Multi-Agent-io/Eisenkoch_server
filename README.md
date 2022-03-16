# Eisenkoch server

This program implements connection between RPI4 and UR3 robot via tcp client-server architecture. 
RPI and robot must be in one network.

To start the program you should install all requirements:
```shell
pip install -r requirements.txt
```
 Then rename and fill in config file:
```shell
mv config_template.yaml config.yaml 
nano config.yaml
```
All information about address and port inside config file.

## Start

To start program run next:
```shell
python3 main.py
```