# IoW-Node

## Introduction

Internet of Wine *(IoW)* is an IoT prototype designed for monitoring of vineyards.
This repo contains the implementation of the sensor node.
The repo of the server can be found here: https://github.com/Hewginn/IoW

## Hardware setup

<img width="500" alt="image" src="https://github.com/user-attachments/assets/5ef637fd-b92a-41e7-a021-99944460d525" />

## Install

- `git clone https://github.com/Hewginn/IoW-Node.git`
- `pip3 install adafruit-circuitpython-dht`
- `pip3 install adafruit-circuitpython-ads1x15`

## Configuration

- In the *config.py* file the ``SERVER_URL`` variable needs to be set to the proper URL.

## Run

- The node is run by calling the *main.py* script: `python3 main.py`
