#!/usr/bin/env python
# coding: utf-8

import amedas
import datetime

def main():
    start = datetime.datetime(2017, 10, 21, 0, 0, 0)

    output_path = "./"
    while True:
        end = datetime.datetime(start.year, start.month, start.day, 23, 59, 59, 999)

        amedas.output_amedas(start, end, amedas)

        start = start + datetime.timedelta(days = 1)
        if start >= datetime.datetime.today():
            break;

if __name__ == '__main__':
    main()
