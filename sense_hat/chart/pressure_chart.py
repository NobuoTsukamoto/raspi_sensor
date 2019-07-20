#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import sqlite3
import datetime

DB_NAME = "/home/pi/DB/sense_hat_weather.db"
TABLE_NAME = "temperature"

def pressureCart(environ, start_response):
    environment = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
    template = environment.get_template('pressure_template.html')

    """ テンプレートに挿入するデータを作成する """
    title = u"Pressure Chart"
    pressure_list = []

    connector = sqlite3.connect(DB_NAME)
    cursor = connector.cursor()
    # sql = "select * from %s where DATE_ADD(date, INTERVAL 24 HOUR) > NOW()" % TABLE_NAME
    sql = "select * from %s" % TABLE_NAME
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        pressure_list.append({'date':record[0], 'pressure':record[4]})
    cursor.close()

    html = template.render({'title':title, 'pressure_list':pressure_list})
    start_response('200 OK', [('Content-Type', 'text/html')])

    return [html.encode('utf-8')]

if __name__ == "__main__":
    from flup.server.fcgi import WSGIServer
    WSGIServer(pressureCart).run()



