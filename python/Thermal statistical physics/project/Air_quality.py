import numpy as np 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import time

mode = 1
def where(wh):
    value = {
        "台北" : "11",
        "新北" : "9",
        "桃園" : "17",
        "新竹" : "24",
        "苗栗" : "26",
        "台中" : "31",
        "彰化" : "33",
        "雲林" : "37",
        "嘉義" : "42",
        "台南" : "46",
        "高雄" : "58",
        "屏東" : "60",
        "台東" : "62",
        "花蓮" : "63",
        "宜蘭" : "65",     
        "澎湖" : "78",
        "基隆" : "1",
        "南投" : "36"            
    }   
    return value.get(wh,"11") 


def Web_crawler(date, wh):  
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome()#chrome_options=options
    driver.get("https://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx")
    select1 = Select(driver.find_element_by_id('ctl05_lbSite'))
    select1.deselect_by_value("84")
    select1.select_by_value(wh)

    select2 = Select(driver.find_element_by_id("ctl05_lbParam"))
    select2.select_by_value("2")
    select2.select_by_value("3")
    select2.select_by_value("4")
    select2.select_by_value("7")

    driver.find_element_by_id("ctl05_txtDateS").clear()
    driver.find_element_by_id("ctl05_txtDateS").send_keys(date)    
    driver.find_element_by_id("ctl05_txtDateE").clear()
    driver.find_element_by_id("ctl05_txtDateE").send_keys(date)    
    driver.find_element_by_id("ctl05_btnQuery").click()

    time.sleep(10)
    #driver.find_element_by_tag_name("td").text
    webdriverlist = driver.find_element_by_id("ctl05_Repeater1_ctl01_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl02_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl03_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl04_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl05_gv").text
    datalist = []
    for i in range(1,10,2):
        tmp = webdriverlist.split("\n")[i].split(" ")
        for i in range(len(tmp)):
            try:
                tmp[i] = float(tmp[i])
            except:
                pass
        datalist.append(tmp)
    print(datalist)
    #driver.close()
    return datalist

def month_last_date(month):
    if(month==0): month=12
    value = {
        1  : 31,
        2  : 28,
        3  : 31,
        4  : 30,
        5  : 31,
        6  : 30,
        7  : 31,
        8  : 31,
        9  : 30,
        10 : 31,
        11 : 30,
        12 : 31
    }   
    return value.get(month,None)


def getdata():
    global day1,day2,mode
    print(entry1.get())
    datehour = entry1.get()
    wh = entry2.get()
    tmp = datehour.split("/")
    date = tmp[0]+"/"+tmp[1]+"/"+tmp[2]
    day1 = Web_crawler(date, where(wh))
    
    if(mode==1):
        if(int(tmp[2])==1):
            if(int(tmp[1])==1): tmp[0]=str(int(tmp[0])-1)
            tmp[2]=str(month_last_date(int(tmp[1])-1))
        else:
            tmp[2]=str(int(tmp[2])-1)
        date = tmp[0]+"/"+tmp[1]+"/"+tmp[2] 
        day2 = Web_crawler(date, where(wh))
        print(day2)
    print(day1)
    

def kind_of_air(kind):
    value = {
        "PM10" : 0,
        "SO2"  : 1,
        "CO"   : 2,
        "O3"   : 3,
        "NO2"  : 4,
    }   
    return value.get(kind,None)    


def graph():
    global mode
    mode = 0
    getdata()
    mode = 1
    index = kind_of_air(entry3.get())
    data = np.zeros(len(day1[index])-1, float)
    for i in range(1,len(day1[index])):
        if(type(day1[index][i])==float):
            data[i-1] = day1[index][i]
        else:
            data[i-1] = -1
    plt.plot(range(1,len(data)+1),data,"-o")
    plt.show()    



print(time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime()) )
#getdata()

window = tk.Tk()
window.title("Air Quality")
window.geometry("680x300")
window.resizable(False, False)

ft = tkFont.Font(size=15, weight=tkFont.BOLD)
label0 = ttk.Label(window, text = "空氣檢測系統", font=(None,25))
label1 = ttk.Label(window, text = "監測時間", font=ft)
label2 = ttk.Label(window, text = "監測地點", font=ft)
label3 = ttk.Label(window, text = "空氣參數", font=ft)

entryText1 = tk.StringVar()
entry1 = ttk.Entry(window, textvariable=entryText1, font=(None,15))
entryText1.set("2019/05/05/11")#"XXXX/XX/XX/XX"

entryText2 = tk.StringVar()
entry2 = ttk.Entry(window, textvariable=entryText2, font=(None,15)) 
entryText2.set("Input the city")

entryText3 = tk.StringVar()
entry3 = ttk.Entry(window, textvariable=entryText3, font=(None,15)) 
entryText3.set("")

botton2 = ttk.Button(window, text = "過去空氣品質", width=20, command = getdata)
botton3 = ttk.Button(window, text = "顯示數據圖", width=20, command = graph)


label0.grid(row=1, column=1, padx=15, pady=15)
label1.grid(row=2, column=0, padx=15, pady=15)
entry1.grid(row=2, column=1, padx=15, pady=15, ipady=5, ipadx=80)
label2.grid(row=3, column=0, padx=15, pady=15)
entry2.grid(row=3, column=1, padx=15, pady=15, ipady=5, ipadx=80)
botton2.grid(row=3, column=2, padx=15, pady=15, ipady=3, ipadx=3)
label3.grid(row=4, column=0, padx=15, pady=15)
entry3.grid(row=4, column=1, padx=15, pady=15, ipady=5, ipadx=80)
botton3.grid(row=4, column=2, padx=15, pady=15, ipady=3, ipadx=3)
window.mainloop()


