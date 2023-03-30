from datetime import datetime
from tkinter import *
import tkinter as tkinter
from tkinter import filedialog
from customtkinter import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

window = CTk()
window.title("Speed Alarm for Modems")
window.geometry("700x500")

checkmarks = {
    'TX': IntVar(value=1),
    'RX': IntVar(value=1),
    '1': IntVar(value=1),
    '3': IntVar(value=0),
    '5': IntVar(value=1),
    '7': IntVar(value=0),
    '11': IntVar(value=0),
    '': IntVar(value=0)
}

mapping = {
    'QPSK': 44,
    '16QAM': 90,
    '32QAM': 112,
    '64QAM': 135,
    '128QAM': 158,
    '256QAM': 181,
    '512QAM': 202,
    '1024QAM': 222,
    '2048QAM': 246
}

outputs = {
    '1': {},
    '2': {},
    '3': {},
    '5': {},
    '6': {},
    '7': {},
    '11': {},
    '12': {}
}
times = {
    '1': [],
    '2': [],
    '3': [],
    '5': [],
    '6': [],
    '7': [],
    '11': [],
    '12': [],
    '': []
}
titles = {
    '1': '',
    '2': '',
    '3': '',
    '5': '',
    '6': '',
    '7': '',
    '11': '',
    '12': ''
}


def choose_file():
    global filename
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select a File", filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))


def create_graph(m1, m2, m3=''):
    times_1 = np.array(times[m1])
    times_2 = np.array(times[m2])
    times_3 = np.array(times[m3])
    sum_times = np.concatenate((times_1, times_2, times_3), axis=None)
    sum_times = np.sort(sum_times)
    sum_times = np.unique(sum_times)
    # do a for loop to add all port 1
    speed_1, speed_2 = [], []
    for t in sum_times:
        if t in outputs[m1]:
            speed_1.append(outputs[m1][t])
        else:
            if len(speed_1) > 0:
                speed_1.append(speed_1[-1])
            else:
                speed_1.append(max(outputs[m1].values()))
        if t in outputs[m2]:
            speed_2.append(outputs[m2][t])
        else:
            if len(speed_2) > 0:
                speed_2.append(speed_2[-1])
            else:
                speed_2.append(max(outputs[m2].values()))

    total_speed = [x + y for x, y in zip(speed_1, speed_2)]
    speed_3 = []

    if len(times[m3]) > 0 and checkmarks[m3].get() == 1:

        for t in sum_times:

            if t in outputs[m3]:
                speed_3.append(outputs[m3][t])
            else:
                if len(speed_3) > 0:
                    speed_3.append(speed_3[-1])
                else:
                    speed_3.append(max(outputs[m3].values()))
        total_speed = [x + y for x, y in zip(total_speed, speed_3)]
    # print(total_speed)
    # get downtime

    totalx = []
    totaly = []
    y1, y2, y3 = [], [], []
    for i in range(len(sum_times)):
        if i > 0:
            totalx.append(sum_times[i])
            totaly.append(totaly[-1])
            y1.append(y1[-1])
            y2.append(y2[-1])
            if len(times[m3]) > 0 and checkmarks[m3].get() == 1:
                y3.append(y3[-1])
        totalx.append(sum_times[i])
        totaly.append(total_speed[i])
        y1.append(speed_1[i])
        y2.append(speed_2[i])
        if len(times[m3]) > 0 and checkmarks[m3].get() == 1:
            y3.append(speed_3[i])

    down_time = 0
    for i in range(1, len(totaly)):
        if totaly[i] < 300 and totaly[i-1] < 300 and totalx[i] != totalx[i-1]:
            print(m1, m2, m3)
            print('time interval caught: ', str(totalx[i-1]), str(totalx[i]))
            print('down time', down_time, 'plus', str(
                (totalx[i]-totalx[i-1]).total_seconds()))
            down_time += (totalx[i]-totalx[i-1]).total_seconds()
    return [y1, y2, y3], [totalx, totaly, down_time]


def onStart():
    global outputs, times, titles
    outputs = {
        '1': {},
        '2': {},
        '3': {},
        '5': {},
        '6': {},
        '7': {},
        '11': {},
        '12': {},
    }

    times = {
        '1': [],
        '2': [],
        '3': [],
        '5': [],
        '6': [],
        '7': [],
        '11': [],
        '12': [],
        '': []
    }
    titles = {
        '1': '',
        '2': '',
        '3': '',
        '5': '',
        '6': '',
        '7': '',
        '11': '',
        '12': ''
    }
    # try:
    month_val = month.get()
    year_val = year.get()
    with open(filename) as f:
        for line in f.read().splitlines():
            line = line.split(",")
            event_time = line[1]
            date_time_obj = datetime.strptime(event_time, '%Y/%m/%d %H:%M:%S')
            modulation = line[9]
            slot_num = line[5]

            if line[10].strip() in mapping and len(slot_num) == 6 and date_time_obj.month == int(month_val) and date_time_obj.year == int(year_val) and ((checkmarks['TX'].get() == 1 and modulation == "TX Modulation") or (checkmarks['RX'].get() == 1 and modulation == "RX Modulation")):
                speed = mapping[line[10].strip()]

                if "0" in slot_num:
                    titles[slot_num[5]] = line[8]
                    times[slot_num[5]].append(date_time_obj)
                    outputs[slot_num[5]][date_time_obj] = speed
                else:
                    titles[slot_num[4:6]] = line[8]
                    times[slot_num[4:6]].append(date_time_obj)
                    outputs[slot_num[4:6]][date_time_obj] = speed
    # except:
    #  print("Error Occured, try again!")
    #  return
    # sorting outputs of all ports
    for k in outputs.keys():
        outputs[k] = {i: outputs[k][i]
                      for i in sorted(list(outputs[k].keys()))}

    modems1, totals1 = create_graph('1', '2', '3')
    modems2, totals2 = create_graph('5', '6', '7')
    modems3, totals3 = [], []
    if len(times['11']) > 0 and len(times['12']) > 0:
        modems3, totals3 = create_graph('11', '12')

    graph_info = [[modems1, totals1], [modems2, totals2], [modems3, totals3]]
    fig, axs = plt.subplots(3, figsize=(12, 12))
    for i in range(3):
        temp1, temp2, temp3 = '', '', ''
        if i == 0:
            temp1 = '1'
            temp2 = '2'
            temp3 = '3'
        elif i == 1:
            temp1 = '5'
            temp2 = '6'
            temp3 = '7'
        else:
            temp1 = '11'
            temp2 = '12'
            temp3 = ''
        if len(graph_info[i][0]) > 0 and len(graph_info[i][1][1]) > 0:
            locator = mdates.AutoDateLocator()

            axs[i].title.set_text(
                titles[temp1]+"     "+"Total time under 300 Mb/s: "+str(graph_info[i][1][2])+" seconds")
            axs[i].set_facecolor('#cccccc')
            axs[i].xaxis.set_minor_locator(mdates.DayLocator(interval=1))
            axs[i].xaxis.set_major_locator(locator)
            axs[i].xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
            axs[i].plot(graph_info[i][1][0], graph_info[i][0]
                        [0], label="Modem "+temp1+" Speed")
            axs[i].plot(graph_info[i][1][0], graph_info[i][0]
                        [1], label="Modem "+temp2+" Speed")
            if temp3 != '':
                if checkmarks[temp3].get() == 1:
                    axs[i].plot(graph_info[i][1][0], graph_info[i]
                                [0][2], label="Modem "+temp3+" Speed")
            axs[i].plot(graph_info[i][1][0], graph_info[i]
                        [1][1], label="Total Speed")
            axs[i].set_alpha(0.5)
            axs[i].legend(loc="lower right")
            axs[i].set_ylim(0, max(graph_info[i][1][1])+50)
            axs[i].grid(True)
            axs[i].set_xlabel('Time')
            axs[i].set_ylabel('Mb/s')

    for l in fig.gca().lines:
        l.set_alpha(.7)
    plt.subplots_adjust(left=0.05, bottom=0.06, right=0.95,
                        top=0.95, wspace=0.2, hspace=0.2)
    plt.show()


greeting = CTkLabel(window, text="Speed Alarm Graphs and Summary for Modems")
greeting.place(relx=0.5, rely=0.1, anchor=CENTER)

file_button = CTkButton(window, text="Choose your Event Log file", command=choose_file,
                        fg_color="#119149", hover_color="#45ba78")
file_button.place(relx=0.5, rely=0.2, anchor=CENTER)
month = CTkEntry(master=window, placeholder_text="Enter a month",
                 width=120, height=25, border_width=2, corner_radius=10)
month.place(relx=0.5, rely=0.3, anchor=CENTER)
year = CTkEntry(master=window, placeholder_text="Enter a year",
                width=120, height=25, border_width=2, corner_radius=10)
year.place(relx=0.5, rely=0.4, anchor=CENTER)

filters = CTkLabel(window, text="Filters")
filters.place(relx=0.5, rely=0.5, anchor=CENTER)


tx = CTkCheckBox(master=window, text="TX", variable=checkmarks['TX'])
tx.place(relx=0.4, rely=0.6, anchor=CENTER)

rx = CTkCheckBox(master=window, text="RX", variable=checkmarks['RX'])
rx.place(relx=0.6, rely=0.6, anchor=CENTER)


m1 = CTkCheckBox(master=window, text="Modem 1/2", variable=checkmarks['1'])
m1.place(relx=0.2, rely=0.7, anchor=CENTER)

m3 = CTkCheckBox(master=window, text="Modem 3", variable=checkmarks['3'])
m3.place(relx=0.35, rely=0.7, anchor=CENTER)

m5 = CTkCheckBox(master=window, text="Modem 5/6", variable=checkmarks['5'])
m5.place(relx=0.5, rely=0.7, anchor=CENTER)

m7 = CTkCheckBox(master=window, text="Modem 7", variable=checkmarks['7'])
m7.place(relx=0.65, rely=0.7, anchor=CENTER)

m11 = CTkCheckBox(master=window, text="Modem 11/12", variable=checkmarks['11'])
m11.place(relx=0.8, rely=0.7, anchor=CENTER)

load_button = CTkButton(window, text="Start", command=onStart,
                        fg_color="#119149", hover_color="#45ba78")
load_button.place(relx=0.5, rely=0.8, anchor=CENTER)

window.mainloop()
