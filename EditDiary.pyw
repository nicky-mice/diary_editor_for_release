#coding:utf-8

import datetime as dt
# import time
#from mimetypes import init
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
# from matplotlib.pyplot import pause
# from numpy import isin
from ttkthemes import *
from subprocess import Popen
# import pyautogui
#from webbrowser import BackgroundBrowser
#import winsound
# import threading



def setup_variables():

    # プログラム開始時刻の取得
    global initialTime
    initialTime = dt.datetime.today()

    # プログラム開始時点での年月日をyyyymmdd形式で取得
    date = initialTime.strftime('%Y%m%d')

    # setting.jsonを開く
    if os.path.isfile('setting.json'):

        # 文字コードの違いにより読み込めない不具合を無くすためUTF-8で開く
        with open('setting.json', 'r', encoding = "utf-8") as jsonFile:

            # setting.jsonの中身を取得
            global settingJson
            settingJson = json.load(jsonFile)
            # return settingJson    

    # 今日の日付.txtのファイル名を取得
    global todaysFileName # 将来的にクラス化したい
    global todaysPathName
    todaysFileName = date + ".txt"
    todaysPathName = os.path.join(settingJson["savePath"] ,todaysFileName)

    global todaysFileLen
    todaysFileLen = 0 # 今日の日付.txtの文字数を格納する変数

    if os.path.isfile(todaysPathName):

        # 文字コードの違いにより読み込めない不具合を無くすためUTF-8で開く
        with open(todaysPathName, encoding = "utf-8") as f:

            # 今日の日付.txtの中身を取得        
            todaysFile = f.read()
            
            # 今日の日付.txtの文字数を取得
            todaysFileLen = len(todaysFile)



def save_text(inputText, path, fileName):

    if path: # pathがNULLである場合のエラー回避
        os.makedirs(path, exist_ok=True) # エラー回避のため、savePathが存在しない場合ディレクトリを作成

        # pathにテキストボックスの内容を追加
        with open(os.path.join(path, fileName), 'a', encoding = 'UTF-8') as fa:
            fa.write('\n' + inputText)


# ボタンが押されたときの処理
#保存して終了
def save_and_quit():

    # inputTextの取得 ０番目～最後(end)まで
    global inputText
    inputText = inputTextBox.get('1.0', 'end')

    # 今日の日付.textにテキストボックスの内容を追加
    save_text(inputText, settingJson["savePath"], todaysFileName)

    # バックアップの保存
    save_text(inputText, settingJson["backupPath"], todaysFileName)

    # プログラムの終了
    root.destroy()

# 過去日記表示
def procA():
    Popen('RemindDiary.pyw', shell=True)


# 文字速度表示のオンオフ切替
def switch_input_speed_display():
    
    inputSpeed.configure(foreground="#424242")

    # global isInputSpeed

    # if isInputSpeed == False:
    #     inputSpeed.configure(foreground="#424242")
    #     isInputSpeed = True

    # else:
    #     inputSpeed.configure(foreground="#ffffff")
    #     isInputSpeed = False


    
# キーイベントの処理
def key_event(event):
    save_and_quit()

    
# プログレスバーの更新
def pb_controller(todaysLen):
    
    targetLen = settingJson["targetLen"] # 一日の目標文字数
    # targetLen = 3000 # 一日の目標文字数

    if todaysLen <= targetLen/6:
        pb.configure(maximum = targetLen/6)
        pbval.set(todaysLen)
        style.configure('TProgressbar', background='lime green', troughcolor='gray80')
    elif todaysLen <= targetLen/2:
        pb.configure(maximum = targetLen/3)
        pbval.set(todaysLen - targetLen/6)
        style.configure('TProgressbar', background='aquamarine3', troughcolor='lime green')
    elif todaysLen <= targetLen:
        pb.configure(maximum = targetLen/2)
        pbval.set(todaysLen - targetLen/2)
        style.configure('TProgressbar', background='light sky blue', troughcolor='aquamarine3')
    elif todaysLen <= targetLen*3:
        pb.configure(maximum = targetLen*2)
        pbval.set(todaysLen - targetLen)
        style.configure('TProgressbar', background='light cyan', troughcolor='light sky blue')
    else:
        pbval.set(targetLen*3)
        style.configure('TProgressbar', background='light cyan', troughcolor='gray80')



# 0.1秒ごとにリアルタイム更新する文字の表示
def show_time():

    # inputTextの取得 ０番目～最後から改行文字を引いた分(end -2 chars)まで
    inputText = inputTextBox.get('1.0', 'end -1 chars')
    
    #入力速度（分速）の計算
    inputSpeed = len(inputText) * 60 / (dt.datetime.today() - initialTime).total_seconds()
    
    # 今日の文字数の計算と表示
    todaysLen = todaysFileLen + len(inputText)
    inputLenDisplay.set('文字数：' + str(todaysLen))

    # プログレスバーの更新
    pb_controller(todaysLen)

    # 入力速度の表示
    inputSpeedDisplay.set('文字数/分：' + str(int(inputSpeed)))

    root.after(100, show_time)


# 効果音の処理
#def local_playsound():
#    winsound.PlaySound("魔王魂 効果音 システム44.wav", winsound.SND_FILENAME)


#def local_playsound_threading(event):
#    t = threading.Thread(target = local_playsound())
#    t.start()


def run_GUI():

    # ここからGUIの処理
    # メインウィンドウ
    # ウィンドウを生成してそのウィンドウを操作するための値をrootに代入します。
    global root
    root = ThemedTk()

    # ウィンドウ名を指定します
    root.title('日記エディタ')
    root.minsize(400, 300)
    # root.maxsize(800, 600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.configure(bg="#424242")


    pad = 10

    # スタイルの設定
    global style
    style = ttk.Style()
    style.theme_use('black')

    fon = Font(family = 'メイリオ', size = 12)
    fon2 = Font(family = 'メイリオ', size = 10)

    # Frame1；ボタン用にtk.Eを設定しないフレーム。tk.Eがあると左寄せできなくなる。
    frame1 = ttk.Frame(root, padding = pad, width = 100)
    frame1.grid(sticky=(tk.N, tk.W))
    frame1.columnconfigure(0, weight=1)
    frame1.rowconfigure(0, weight=1)
    # frame1.grid_propagate(False)
    # style.configure('TFrame', background = 'gray50')

    # frame3
    # frame3 = ttk.Frame(root, padding = pad, width = 100)
    # frame3.grid(sticky=(tk.N, tk.S, tk.E))
    # frame3.columnconfigure(1, weight=1)
    # frame3.rowconfigure(0, weight=1)
    # style.configure('TFrame', background = 'green')

    # frame2：テキストボックス用フレーム。column1以降に配置するウィジェットがあるとスクロールバーが正常に配置できない。
    frame2 = ttk.Frame(root, padding = pad, width = 100)
    frame2.grid(sticky=(tk.N, tk.W, tk.S, tk.E))
    frame2.columnconfigure(0, weight=1)
    frame2.rowconfigure(1, weight=1)
    # style.configure('TFrame', background = 'green')



    # ボタンの定義
    ButtonA = tk.Button(frame1,text="過去日記表示", command=procA, width=12, height=2)
    ButtonA.configure(bg="#C2C2C2", font = fon2)

    # ButtonB = tk.Button(frame1,text="合計文字数", command=procB, width=12, height=2)
    ButtonC = tk.Button(frame1,text="保存", command=save_and_quit, width=12, height=2)
    ButtonC.configure(bg="#C2C2C2", font = fon2)

    # キーイベントの定義
    # Ctrl + Shift + sで保存して終了
    root.bind('<Control-Key-S>', key_event)

    # キープレスで効果音再生
    # root.bind('<Key>', local_playsound_threading)

    # 現在の周回での目標文字数の定義
    # inputMaximum = tk.StringVar()
    # inputMaximum.set('')

    # 今日の入力文字数の表示の定義
    global inputLenDisplay
    inputLenDisplay = tk.StringVar()
    inputLenDisplay.set('')
    inputLen = ttk.Label(frame2, text = '今日の入力文字数', textvariable = inputLenDisplay)
    inputLen.configure(font = fon2)

    # プログレスバー (確定的)
    global pbval
    pbval = tk.IntVar()

    global pb
    pb = ttk.Progressbar(
        frame2,
        orient = tk.HORIZONTAL,
        variable = pbval,
        mode='determinate')

    # 文字入力速度の表示の定義
    global inputSpeedDisplay
    inputSpeedDisplay = tk.StringVar()

    inputSpeedDisplay.set('')

    global inputSpeed
    inputSpeed = ttk.Label(frame2, text = '文字入力速度', textvariable = inputSpeedDisplay)
    inputSpeed.configure(font = fon2, foreground="#ffffff")

    # 入力文字速度をクリックしたときのキーイベントを定義
    inputSpeed.bind("<Button-1>", lambda event : switch_input_speed_display())


    # 入力テキストボックスの定義
    global inputTextBox
    inputTextBox = tk.Text(frame2, bg = '#222222', fg = 'white', insertbackground='white', undo=True, height = 15, width = 70)
    inputTextBox.configure(font = fon)

    # 入力テキストボックスのScrollbar
    scrollbar = ttk.Scrollbar(
        frame2,
        orient = tk.VERTICAL,
        command = inputTextBox.yview
        )



    # widgetの配置
    #ボタンの配置
    ButtonA.grid(row=0, column=0, pady=5, sticky=(tk.N, tk.W))
    ButtonC.grid(row=0, column=1, pady=5, sticky=(tk.N, tk.W))

    # ButtonB.grid(row=0, column=2, pady=5, sticky=tk.W)


    # 現在の周回での目標文字数の表示
    # ttk.Label(frame3, textvariable = inputMaximum).grid(row=0, column=0, padx=5, pady=5, sticky = (tk.N, tk.W, tk.E))


    # プログレスバーの配置
    pb.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.E, tk.W))

    # 今日の入力文字数の配置
    inputLen.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky = (tk.N, tk.W, tk.S, tk.E))

    # 文字入力速度の配置
    inputSpeed.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky = (tk.N, tk.W, tk.S, tk.E))

    # テキストボックスの配置
    inputTextBox.grid(row = 4, column = 0, sticky = (tk.N, tk.W, tk.S, tk.E))

    # スクロールバーの配置
    scrollbar.grid(row=4, column=1, sticky=(tk.N, tk.S))

    # テキストボックスにフォーカスを合わせる
    inputTextBox.focus_set()

    #Popen("Change2Kana", shell=True)




    show_time()

    # ウィンドウを表示して制御するためのループに入る
    root.mainloop()


if __name__ == "__main__":
    setup_variables()
    run_GUI()