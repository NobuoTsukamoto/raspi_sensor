#!/usr/bin/env python
# coding: utf-8

import amedas
import datetime

def main():
    output_path = "/home/pi/Amedas/Day"
    yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
    start = datetime.datetime(yesterday.year, yesterday.month, yesterday.day,
            0, 0, 0, 0)
    end = datetime.datetime(yesterday.year, yesterday.month, yesterday.day,
            23, 59, 59, 999)

    amedas.output_amedas(start, end, output_path)

if __name__ == '__main__':
    main()
