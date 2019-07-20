#!/usr/bin/env python
# coding: utf-8

import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DB_NAME = "/home/pi/DB/sense_hat_weather.db"
#DB_NAME = "/home/nobuo/Workspese/raspi_sensor/sense_hat_weather.db"
TABLE_NAME = "temperature"

def get_db_data(start, end):
    """ 指定した期間のグラフを出力する

    Args:
        start: 取得する開始(datetime)
        end: 取得する終了(datetime)

    Returns:
        DBから取得したデータ(配列)
    """

    amedas_data = []

    try:
        start_date = start.strftime("%Y-%m-%d %H:%M:%S.%f")
        end_date = end.strftime("%Y-%m-%d %H:%M:%S.%f")

        connecter = sqlite3.connect(DB_NAME)
        cursor = connecter.cursor()

        sql = "select * from %s where date between '%s' and '%s'" % \
                (TABLE_NAME, start_date, end_date)
        cursor.execute(sql)
        amedas_data = cursor.fetchall()

    except Exception as e:
        print("Exception")
        print(e)
        print("type : ", type(e))
        print("args : ",  e.args)
        print("message : ", e.message)

    finally:
        cursor.close()
        connecter.close()

    return amedas_data

def save_plot_data(date, temp, humidity, pressure, save_path = "./"):
    """ アメダスデータをグラフに描画して保存する

    Args:
        date: 観測時間
        temp: 気温
        humidity: 湿度
        pressure: 気圧
        save_path: 画像の出力フォルダ
    """

    days = mdates.AutoDateLocator()
    days_format = mdates.DateFormatter("%m/%d %H:%M")

    fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize=(19.2, 10.8))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.3)

    # 気温を描画する
    ax[0, 0].plot(date, temp, linestyle='solid', linewidth = 1.0, marker= ".")
    ax[0, 0].set_title("temperature")
    ax[0, 0].set_xlabel("date")
    ax[0, 0].set_ylabel("degrees Celsius")
    ax[0, 0].set_ylim(-5, 40)
    ax[0, 0].grid(True)
    ax[0, 0].xaxis.set_major_locator(days)
    ax[0, 0].xaxis.set_major_formatter(days_format)
    plt.setp(ax[0, 0].get_xticklabels(), rotation = 20)

    # 湿度を描画する
    ax[0, 1].plot(date, humidity, linestyle='solid', linewidth = 1.0, marker= ".")
    ax[0, 1].set_title("humidity")
    ax[0, 1].set_xlabel("date")
    ax[0, 1].set_ylabel("%")
    ax[0, 1].set_ylim(0, 100)
    ax[0, 1].grid(True)
    ax[0, 1].xaxis.set_major_locator(days)
    ax[0, 1].xaxis.set_major_formatter(days_format)
    plt.setp(ax[0, 1].get_xticklabels(), rotation = 20)

    # 気圧を描画する
    ax[1, 0].plot(date, pressure, linestyle='solid', linewidth = 1.0, marker= ".")
    ax[1, 0].set_title("pressure")
    ax[1, 0].set_xlabel("date")
    ax[1, 0].set_ylabel("hPa")
    #ax[1, 0].set_ylim(960, 1060)
    ax[1, 0].grid(True)
    ax[1, 0].xaxis.set_major_locator(days)
    ax[1, 0].xaxis.set_major_formatter(days_format)
    plt.setp(ax[1, 0].get_xticklabels(), rotation = 20)

    ax[1, 1].axis("off")

    # 保存するためのファイル名を作成
    # ファイル名の形式(amedas_yyyymmddhhmmdd_
    start = date[0]
    end = date[-1]
    file_name = save_path + "/" + "amedas_" + start.strftime("%Y%m%d%H%M") + "_" \
                + end.strftime("%Y%m%d%H%M") + ".png"

    plt.savefig(file_name)

    print("output file : " + file_name)


def change_db_to_plot_data(data):
    """ DBの生データを表示用のデータに加工する

        生成するリストは
        ・時間(datetime), YYYY/MM/DD HH:MM:SS まで
        ・温度(CPU温度による補正)
        ・湿度
        ・気圧(海抜0m基準)

        T.B.D.
        欠損データがある場合(時間が飛んでいる)はレコードを新規作成するか？
        (時刻データとNULLデータを生成する)

    Args:
        data: アメダスデータの配列
    Returns:
        date_list: 取得日時
        temp_list: 気温
        humidity_list: 湿度
        pressure_list: 気圧
    """

    # 標高
    elevation = 386.0000

    # 各リストを初期化
    date_list = []
    temp_list = []
    humidity_list = []
    pressure_list = []

    for i in data:
        # 時刻をdatetimeで追加
        date_list.append(datetime.datetime.strptime(i[0],
            '%Y-%m-%d %H:%M:%S.%f'))

        # 温度, 以下の公式で補正
        # AmbientTemp - ( (CPUtemp - AmbientTemp) / 2 )
        temp = i[2] - ((i[5] - i[2]) / 2)
        temp_list.append(temp)

        # 湿度
        humidity_list.append(i[1])

        # 大気圧
        # 即高公式で補正
        # p=p0(1-0.0065z/(t0+273.15))^5.257
        # p0 地上気圧, t0 地上気温, z 標高
        p = i[4] * (1 - (0.0065 * elevation) / (temp + 273.15)) ** -5.257
        pressure_list.append(p)

    return date_list, temp_list, humidity_list, pressure_list

def output_amedas(start, end, path):
    """ 指定区間のアメダスデータを出力する

    Args:
        start: 開始日時
        end: 終了日時
        path: 出力フォルダ
    """

    amedas_data = get_db_data(start, end)
    date, temp, humidity, pressure = change_db_to_plot_data(amedas_data)
    save_plot_data(date, temp, humidity, pressure, path)


