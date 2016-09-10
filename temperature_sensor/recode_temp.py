# usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import wiringpi as wp
import sqlite3

SPI_CH = 0      # SPI channle
PIN_BASE = 70   # pin base(above 64)

DB_NAME = "/home/pi/DB/sensor.db"
TABLE_NAME = "temperature"

def getTemperature():
    """MCP3002からアナログ値を取得する

    wiringpi2のMCP3002 Extensionを利用して、アナログ値を取得する
    PIN_BASEは、handleのような形で使用する
    ただし、予め64より大きい値を指定しておく必要がある
    取得したアナログ値（電圧値）を温度に変換する

    温度センサー(hcp9700e)の仕様
      電圧範囲は100mVから1.75V
      0℃の時には500mVの出力電圧
      温度の係数は10.0mV/℃
      1℃につき10mV出力電圧が変化

    温度の求め方
      MCP3002の出力は10bit(1024)
      SPIの出力電圧3.3V(=3300mV)を10bitのステップで計算
        電圧mV = (出力値 * 3300mV) / 1024
      0℃を基準として温度を計算
        温度℃  = (電圧mV - 500mV) / 10mV/℃

    Returns:
        温度（小数点型）

    """

    wp.mcp3002Setup(PIN_BASE, SPI_CH)
    wp.wiringPiSetupGpio()
    value = wp.analogRead(PIN_BASE)

    temprature = (value * 3300) / 1024
    temprature = (temprature - 500) / 10
    temprature = round(temprature, 1)

    return temprature

def WriteDatabase(value):
    try:
        connector = sqlite3.connect(DB_NAME)
        cursor = connector.cursor()
        sql = "select count(*) from sqlite_master where type='table' and name='%s'" % TABLE_NAME
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] == 0:
            print("table is not exsit. create table")

            cursor.execute("create table %s(date text, value real);" % TABLE_NAME)
            connector.commit()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        sql = "insert into %s values ('%s', %f)" % (TABLE_NAME, now, value)
        cursor.execute(sql)
        connector.commit()
        cursor.close()
        connector.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    value = getTemperature()
    print("temperature %f" % value)
    WriteDatabase(value)
