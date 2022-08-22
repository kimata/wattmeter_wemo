#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywemo


def get_power_list():
    devices = pywemo.discover_devices()

    power_list = []
    for dev in devices:
        if dev.__class__ is not pywemo.ouimeaux_device.insight.Insight:
            continue

        power_list.append(
            {
                "name": dev.name,
                "power": dev.insight_params["currentpower"] / 1000.0,
            }
        )

    return power_list
