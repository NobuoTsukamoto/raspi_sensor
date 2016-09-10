#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import datetime
from tkinter import *

DB_NAME = "./sensor.db"
TABLE_NAME = "temperature"

def PlotTemperature(date):
    try:
        date_list = []
        temp_list = []
        connector = sqlite3.connect(DB_NAME)
        cursor = connector.cursor()
        sql = "select * from %s where date like \'%s %%\'" % (TABLE_NAME, date)
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            date_list.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
            temp_list.append(row[1])

        plt.figure(figsize=(16,5))
        plt.plot(date_list, temp_list, "b")
        plt.savefig("graph_" + date + ".png")
        cursor.close()
        connector.close()
    except Exception as e:
        print("Exception: " + e)

if __name__ == "__main__":
    PlotTemperature("2016-09-10")
