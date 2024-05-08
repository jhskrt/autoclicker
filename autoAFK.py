from pydirectinput import press

from tkinter import *

# from msvcrt import getch
from time import time, sleep
from datetime import datetime
from random import uniform


class AutoAFK:
    def __init__(self, win):

        self.win = win
        self.topmost = True
        win.title("Auto AFK")
        win.geometry('380x300')
        win.resizable(False, False)
        win.attributes('-topmost', self.topmost)

        # set topmost
        self.topmost_var = BooleanVar(value=True)
        self.topmost_checkbutton = Checkbutton(
            text='是否置頂',
            command=self.set_topmost,
            variable=self.topmost_var
        )
        self.topmost_checkbutton.pack(side='top')

        # status label
        self.status_label = Label(text='狀態: 尚未開始')
        self.status_label.pack(side='top')

        # mode select menu
        self.cooldown_var = StringVar()
        self.button_var = StringVar()

        self.select_cooldown = Entry(textvariable=self.cooldown_var)
        self.select_button = Entry(textvariable=self.button_var)

        cooldown_label = Label(text="輸入按鍵間隔(s)")
        button_label = Label(text="輸入按鍵 以空格隔開")

        cooldown_label.pack()
        self.select_cooldown.pack()
        button_label.pack()
        self.select_button.pack()

        # show start time
        self.time_label = Label(text='開始時間: N/A')
        self.time_label.pack(side='top')

        # show elapsed time
        self.elapsed_time_label = Label(text='執行時間: N/A')
        self.elapsed_time_label.pack(side='top')

        # show counter
        self.counter_label = Label(text="執行次數: 0")
        self.counter_label.pack()

        # show avg press time
        self.avg_label = Label(text='平均執行間隔: N/A')
        self.avg_label.pack()

        # next press time
        self.next_press_label = Label(text='下次執行時間: N/A')
        self.next_press_label.pack()

        # stop btn
        self.stop_button = Button(text='暫停', command=self.stopButtonCmd)
        self.stop_button.pack(side='bottom')
        self.stop_button.config(state=DISABLED)

        # start btn
        self.start_button = Button(text='開始', command=self.startButtonCmd)
        self.start_button.pack(side='bottom')

        self.is_running = False
        self.cooldown = 1.0
        self.now_time = None
        self.start_time = None
        self.elapsed_time = None
        self.counter = 0
        self.total_sleep_time = 0
        self.avg_sleep_time = 0

    # update topmost

    def set_topmost(self):
        self.topmost = self.topmost_var.get()
        win.attributes('-topmost', self.topmost)

    def startButtonCmd(self):
        self.start_time = time()
        self.start_datetime = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=f'開始時間: {self.start_datetime}')
        self.update_time()
        print(f'===\nStarts at {self.start_datetime}\n===')

        self.is_running = True
        self.main()

        self.status_label.config(text='狀態: 執行中')
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.select_cooldown.config(state=DISABLED)
        self.select_button.config(state=DISABLED)

    def stopButtonCmd(self):
        print(f'===\nPaused at {self.now_time}\n===')

        self.is_running = False

        self.status_label.config(text='狀態: 暫停中')

        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.select_cooldown.config(state=NORMAL)
        self.select_button.config(state=NORMAL)

    def update_label(self):
        self.counter_label.config(text=f'執行次數: {self.counter}')
        self.avg_label.config(
            text=f'平均執行間隔: {round(self.total_sleep_time/self.counter, 5)}')

    def update_time(self):
        self.now_time = datetime.now().strftime('%H:%M:%S')
        elapsed_time = time() - self.start_time

        minutes = int(elapsed_time / 60)
        seconds = int(elapsed_time % 60)

        self.elapsed_time = f'{minutes:02d} : {seconds:02d}'
        self.elapsed_time_label.config(text=f'執行時間: {self.elapsed_time}')

        self.win.after(1000, self.update_time)

    def main(self):
        if not self.is_running:
            return

        press_buttons = self.button_var.get().split(" ")
        press_buttons = list(map(lambda s: s.lower(), press_buttons))

        press(press_buttons[self.counter % len(press_buttons)])

        self.counter += 1
        self.cooldown = float(self.select_cooldown.get())

        sleepTime = uniform(self.cooldown+self.cooldown*0.05,
                            self.cooldown-self.cooldown*0.05)
        print(f"{self.counter} {sleepTime}")

        self.update_label()
        self.next_press_label.config(text=f'下次執行時間: {round(sleepTime, 2)}')

        self.total_sleep_time += sleepTime
        sleepTime *= 1000
        sleepTime = round(sleepTime)
        self.win.after(sleepTime, self.main)


win = Tk()
gui = AutoAFK(win)
print('windows successfully opened!')
win.mainloop()
