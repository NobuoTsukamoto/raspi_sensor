# usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import time
import datetime
import sqlite3
from sense_hat import SenseHat


DB_NAME = "/home/pi/DB/sense_hat_weather.db"
TABLE_NAME = "temperature"

def getCpuTemparature():
    process = subprocess.Popen(["vcgencmd", "measure_temp"],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
    process.wait()
    read_result = process.stdout.read()
    temp_string = read_result.decode('utf-8')
    match_result = re.findall("[0-9.]+", str(read_result))
    return float(match_result[0])

def WriteDatabase():
    """DBに気象データを書き込む

    DBにテーブルが存在しない場合は、テーブルを作成する。
    作成するテーブルの定義
      項目名                カラム名        型
      日時                  date            text
      湿度                  humidity        teal
      温度(湿度センサー)    temp_humidity   real
      温度(気圧センサー)    temp_pressure   real
      気圧                  pressure        real
      CPU温度               cpu_temp        real

    温度値はsens-hatとraspberry piの基盤が近いため、
    raspberry piのCPUの発熱に影響を受ける。
    補正を行うために、CPU温度も記録する。

    Args:

    """

    try:
        connector = sqlite3.connect(DB_NAME)
        cursor = connector.cursor()
        sql = "select count(*) from sqlite_master where type='table' and name='%s'" % TABLE_NAME
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] == 0:
            print("table is not exsit. create table")

            cursor.execute("create table %s(date text, humidity real, temp_humidity real, temp_pressure real, pressure real, cpu_temp real);" % TABLE_NAME)
            connector.commit()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        sense = SenseHat()
        humidity = sense.get_humidity()
        temp_humidity = sense.get_temperature_from_humidity()
        temp_pressure = sense.get_temperature_from_pressure()
        cpu_temp = getCpuTemparature()
        pressure = sense.get_pressure()
        sql = "insert into %s values ('%s', %f, %f, %f, %f, %f)" % (TABLE_NAME, now, humidity, temp_humidity, temp_pressure, pressure, cpu_temp)
        cursor.execute(sql)
        connector.commit()
        cursor.close()
        connector.close()

        print(humidity, temp_humidity, temp_pressure, pressure, cpu_temp)
    except Exception as e:
        print("----- Exception -----")
        print("type : " + type(e))
        print("args : " + e.args)
        print("message : " + e.message)
        print(e)

if __name__ == "__main__":
    WriteDatabase()
