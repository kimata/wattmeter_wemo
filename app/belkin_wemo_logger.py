#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import pathlib
import datetime
import time
import fluent.sender

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "lib"))

import wemo_insight
from config import load_config
import logger

DEV_CONFIG = "../device.yml"


def get_label(dev_list, name):
    for dev_info in dev_list:
        if dev_info["name"] == name:
            return dev_info["label"]
    return None


def fluent_send(sender, power_list, dev_list):
    for power_info in power_list:
        label = get_label(dev_list, power_info["name"])

        if label is None:
            logging.warning("Unkown device: {name}".format(name=power_info["name"]))
            continue

        data = {
            "hostname": label,
            "power": int(power_info["power"]),
        }

        if sender.emit("wemo", data):
            logging.info("Send: {data}".format(data=str(data)))
            pathlib.Path(config["liveness"]["file"]).touch()
        else:
            logging.error(sender.last_error)


######################################################################
logger.init("hems.wattmeter.wemo")

logging.info("Load config...")
config = load_config()
dev_list = load_config(DEV_CONFIG)

sender = fluent.sender.FluentSender("hems", host=config["fluent"]["host"])

while True:
    logging.info("Start.")

    fluent_send(sender, wemo_insight.get_power_list(), dev_list)

    logging.info("Finish.")
    pathlib.Path(config["liveness"]["file"]).touch()

    sleep_time = config["sense"]["interval"] - datetime.datetime.now().second
    logging.info("sleep {sleep_time} sec...".format(sleep_time=sleep_time))
    time.sleep(sleep_time)
