#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import sqlite3
import datetime

DB_NAME = "/home/pi/DB/sense_hat_weather.db"
TABLE_NAME = "temperature"

def humidityCart(environ, start_response):
    environment = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
    template = environment.get_template('humidity_template.html')

    """ テンプレートに挿入するデータを作成する """
    title = u"Humidity Chart"
    humidity_list = []

    connector = sqlite3.connect(DB_NAME)
    cursor = connector.cursor()
    # sql = "select * from %s where DATE_ADD(date, INTERVAL 24 HOUR) > NOW()" % TABLE_NAME
    sql = "select * from %s" % TABLE_NAME
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        humidity_list.append({'date':record[0], 'humidity':record[1]})
    cursor.close()

    html = template.render({'title':title, 'humidity_list':humidity_list})
    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(humidityCart).run()



