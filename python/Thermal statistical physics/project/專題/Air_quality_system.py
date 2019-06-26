import numpy as np 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import matplotlib.pylab as plt
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import time,copy

################################################################

Internet_waiting_time = 10                     #網路等待時間(s)
air_valid_time = [24,5,8,4,5]                  #有效時間(hr)
data_base_range = ["2019/01/01","2019/05/30"]  #資料庫範圍

################################################################

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
    return value.get(wh,"31") 

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

def kind_of_air(kind):
    value = {
        "PM10" : 0,
        "SO2"  : 1,
        "CO"   : 2,
        "O3"   : 3,
        "NO2"  : 4
    }   
    return value.get(kind,None) 

def unit(kind):
    value = {
        "PM10" : "μg/m3",
        "SO2"  : "ppb",
        "CO"   : "ppm",
        "O3"   : "ppb",
        "NO2"  : "ppb"
    }   
    return value.get(kind,None)

def yesterday(date):
    temp = date.split("/")
    if(int(temp[2])==1):
        temp[2]=str(month_last_date(int(temp[1])-1))
        if(int(temp[1])==1): 
            temp[0]=str(int(temp[0])-1)
            temp[1]="12"
        else:
            temp[1]=str(int(temp[1])-1)            
    else:
        temp[2]=str(int(temp[2])-1)
    y = ""
    for i in range(len(temp)-1):
        y += temp[i]+"/"
    y += temp[-1]
    return y

def data_base(year, month, day):
    start = data_base_range[0]
    end   = data_base_range[1]   
    flag = 0
    if(year>int(start.split("/")[0])):
        flag += 1
    elif(year==int(start.split("/")[0])):
        if(month>int(start.split("/")[1])):
            flag += 1
        elif(month==int(start.split("/")[1])):
            if(day>=int(start.split("/")[2])):
                flag += 1
    if(year<int(end.split("/")[0])):
        flag += 1
    elif(year==int(end.split("/")[0])):
        if(month<int(end.split("/")[1])):
            flag += 1
        elif(month==int(end.split("/")[1])):
            if(day<=int(end.split("/")[2])):
                flag += 1
    if(flag==2):
        judge=True
    else:
        judge=False
    return judge

def formula(quality_data):
    def air(mode,inputdata):
        def PM10(data):
            if(data>=0 and data<35):
                q = 1
            elif(data>=35 and data<60):
                q = 2
            elif(data>=60 and data<75):
                q = 3
            elif(data>=75 and data<100):
                q = 4
            elif(data>=100):
                q = 5 
            return q      
        def SO2(data):
            if(data>=0 and data<30):
                q = 1
            elif(data>=30 and data<140):
                q = 2
            elif(data>=140 and data<200):
                q = 3
            elif(data>=200 and data<300):
                q = 4
            elif(data>=300):
                q = 5 
            return q 
        def CO(data):
            if(data>=0 and data<5):
                q = 1
            elif(data>=5 and data<10):
                q = 2
            elif(data>=10 and data<15):
                q = 3
            elif(data>=15 and data<30):
                q = 4
            elif(data>=30):
                q = 5 
            return q   
        def O3(data):
            if(data>=0 and data<60):
                q = 1
            elif(data>=60 and data<130):
                q = 2
            elif(data>=130 and data<200):
                q = 3
            elif(data>=200 and data<400):
                q = 4
            elif(data>=400):
                q = 5 
            return q 
        def NO2(data):        
            if(data>=0 and data<300):
                q = 1
            elif(data>=300 and data<600):
                q = 2
            elif(data>=600 and data<1200):
                q = 3
            elif(data>=1200 and data<1600):
                q = 4
            elif(data>=1600):
                q = 5 
            return q 
        value = {
            0 : PM10(inputdata),
            1 : SO2(inputdata),
            2 : CO(inputdata),
            3 : O3(inputdata),
            4 : NO2(inputdata)
        }   
        return value.get(mode,None)             

    quality_number = 0    
    for i in range(len(quality_data)):
        quality_number += (air(i,quality_data[i]))**3
    quality_number = (quality_number/len(quality_data))*100/125
    if(quality_number<=20.64):
        quality_number = quality_number*4
    else:
        quality_number = 20.64*4 + (quality_number-20.64)*(100-20.64*4)/(100-20.64)
    if(quality_number<=10.88):
        quality_number = quality_number*6
    elif(quality_number<20.64*4):
        quality_number = 10.88*6 + (quality_number-10.88)*(20.64*4-10.88*6)/(20.64*4-10.88)
    if(quality_number<=4.96):
        quality_number = quality_number*8
    elif(quality_number<10.88*6):
        quality_number = 4.96*8 + (quality_number-4.96)*(10.88*6-4.96*8)/(10.88*6-4.96)
    if(quality_number<=1.92):
        quality_number = quality_number*10
    elif(quality_number<4.96*8):
        quality_number = 1.92*10 + (quality_number-1.92)*(4.96*8-1.92*10)/(4.96*8-1.92)
    return round(quality_number,2)

def Quality(day1,day2,hour):
    times = air_valid_time
    hour -= 1
    
    data = []
    if(hour==0): hour = 23
    for i in range(len(times)):
        tmp = []
        for j in range(hour+1,0,-1):
            if(type(day1[i][j])==float):
                tmp.append(day1[i][j])
                times[i] -= 1
            elif(times[i]==0):
                break
        for j in range(23+1,0,-1):
            if(type(day2[i][j])==float):
                tmp.append(day2[i][j])
                times[i] -= 1
            elif(times[i]==0):
                break   
        data.append(copy.copy(tmp))  

        quality_data = []
        for i in range(len(data)):
            sum = 0
            for j in range(len(data[i])):
                sum += data[i][j]
            quality_data.append(sum/len(data[i]))
    return formula(quality_data)

def grade(quality_number):
    if(quality_number>=0 and quality_number<1.92*10):
        s = "空氣品質優良"
    elif(quality_number>=1.92*10 and quality_number<4.96*8):
        s = "空氣品質普通"
    elif(quality_number>=4.96*8 and quality_number<10.88*6):
        s = "對少數敏感族群不佳" 
    elif(quality_number>=10.88*6 and quality_number<20.64*4):
        s = "不建議出遊" 
    elif(quality_number>=20.64*4 and quality_number<=100):
        s = "請把握當下"            
    else:
        s = "program error"
    return s

def close():
    try:
        window1.destroy()
    except:
        pass 
    try:
        window3.destroy()
    except:
        pass    

def Web_crawler(date, wh):  
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)#chrome_options=options

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
    driver.find_element_by_id("ctl05_txtDateE").send_keys(Keys.ENTER)

    time.sleep(3)
    driver.find_element_by_id("ctl05_btnQuery").click()

    time.sleep(Internet_waiting_time)
    webdriverlist = driver.find_element_by_id("ctl05_Repeater1_ctl04_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl01_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl02_gv").text
    webdriverlist += "\n"+driver.find_element_by_id("ctl05_Repeater1_ctl03_gv").text
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
    print("crawler the data successful...")
    driver.close()
    return datalist

def history_getdata(): 
    try:
        global day1,day2,mode,window1    
        datehour = entry1.get()
        wh = entry2.get()
        tmp = datehour.split("/")    
        ytmp = yesterday(datehour).split("/")
        hour = tmp[3]

        if(data_base(int(tmp[0]),int(tmp[1]),int(tmp[2])) and 
            data_base(int(ytmp[0]),int(ytmp[1]),int(ytmp[2]))):
            air = ["PM10","SO2","CO","O3","NO2"]
            data = []

            for i in air:
                f = open("./data/"+wh+"/"+wh+i+".txt",'r')
                line = f.readline()
                flag = 0
                while line:
                    try:
                        if(int(line[0])==0 or int(line[0])==1):
                            if(flag==1 or (int(line.split(" ")[0].split("/")[0])==int(ytmp[1]) and
                                int(line.split(" ")[0].split("/")[1])==int(ytmp[2]))):
                                flag += 1
                                data.append(line)
                    except:
                        pass            
                    line = f.readline()
                    if(flag==2): break
                f.close()

            day1 = []
            day2 = []
            for i in range(1,10,2):
                tmp = []
                for j in data[i].split(" "):
                    try:
                        tmp.append(float(j))
                    except:
                        tmp.append(j)
                day1.append(tmp)
            for i in range(0,10,2):
                tmp = []
                for j in data[i].split(" "):
                    try:
                        tmp.append(float(j))
                    except:
                        tmp.append(j)
                day2.append(tmp)

            if(mode==1):
                window1 = tk.Tk()
                window1.title("result")
                window1.geometry("320x200")
                window1.resizable(False, False) 
                blank1 = ttk.Label(window1, text = "    ", font=(None,15)) 
                label1 = ttk.Label(window1, text = "< 空氣品質檢測結果 >", font=(None,20)) 
                label2 = ttk.Label(window1, text = "空氣指數 : "+str(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
                label3 = ttk.Label(window1, text = "出遊建議 : "+grade(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
                button = ttk.Button(window1, text = "關閉", command = close)
                blank1.grid(row=0,column=0,pady=10)    
                label1.grid(row=0,column=1,pady=15)
                label2.grid(row=1,column=1,pady=10)
                label3.grid(row=2,column=1,pady=10)
                blank1.grid(row=3,column=0,pady=10)  
                button.grid(row=3,column=1,pady=10)

                window1.mainloop() 
        else:  
            window2 = tk.Tk()
            window2.title("alert")
            window2.geometry("300x200")
            window2.resizable(False, False) 
            label = ttk.Label(window2, text = " Wait for about 30 second...",font=(None,20))
            label0 = ttk.Label(window2, text = " We need to crawler the data...",font=(None,15))
            label.grid(pady=25)
            label0.grid(pady=25)
            window2.update_idletasks()
            window2.update()

            date = tmp[0]+"/"+tmp[1]+"/"+tmp[2]
            day1 = Web_crawler(date, where(wh))   
            if(mode==1):
                date = ytmp[0]+"/"+ytmp[1]+"/"+ytmp[2] 
                day2 = Web_crawler(date, where(wh))
                
                print("quality_number : "+str(Quality(day1,day2,int(datehour.split("/")[-1]))))
                print(grade(Quality(day1,day2,int(datehour.split("/")[-1]))))
                window2.destroy()

                window1 = tk.Tk()
                window1.title("result")
                window1.geometry("320x200")
                window1.resizable(False, False) 
                blank1 = ttk.Label(window1, text = "    ", font=(None,15)) 
                label1 = ttk.Label(window1, text = "< 空氣品質檢測結果 >", font=(None,20)) 
                label2 = ttk.Label(window1, text = "空氣指數 : "+str(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
                label3 = ttk.Label(window1, text = "出遊建議 : "+grade(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
                button = ttk.Button(window1, text = "關閉", command = close)
                blank1.grid(row=0,column=0,pady=10)    
                label1.grid(row=0,column=1,pady=15)
                label2.grid(row=1,column=1,pady=10)
                label3.grid(row=2,column=1,pady=10)
                blank1.grid(row=3,column=0,pady=10)  
                button.grid(row=3,column=1,pady=10)

                window1.mainloop()
            else:
                window2.destroy()
    except:
        global window3
        window3 = tk.Tk()
        window3.title("alert")
        window3.geometry("300x200")
        window3.resizable(False, False) 
        label = ttk.Label(window3, text = "    Please input the correct information",font=(None,15))
        label0 = ttk.Label(window3, text = "    Please check your internet",font=(None,15))
        button = ttk.Button(window3, text = "關閉", command = close)
        label.grid(pady=20)
        label0.grid(pady=20)
        button.grid(pady=20)
        window3.mainloop()
      

def instant_getdata():  
    try:
        global window1 
        datehour = time.strftime("%Y/%m/%d/%H", time.localtime())
        wh = entry2.get()
        tmp = datehour.split("/")
        ytmp = yesterday(datehour).split("/")

        window2 = tk.Tk()
        window2.title("alert")
        window2.geometry("300x200")
        window2.resizable(False, False) 
        label = ttk.Label(window2, text = " Wait for about 30 second...",font=(None,20))
        label0 = ttk.Label(window2, text = " We need to crawler the data...",font=(None,15))
        label.grid(pady=25)
        label0.grid(pady=25)
        window2.update_idletasks()
        window2.update()

        date = tmp[0]+"/"+tmp[1]+"/"+tmp[2]
        day1 = Web_crawler(date, where(wh))    
        date = ytmp[0]+"/"+ytmp[1]+"/"+ytmp[2] 
        day2 = Web_crawler(date, where(wh))

        print("quality_number : "+str(Quality(day1,day2,int(datehour.split("/")[-1]))))
        print(grade(Quality(day1,day2,int(datehour.split("/")[-1]))))
        window2.destroy()

        window1 = tk.Tk()
        window1.title("result")
        window1.geometry("320x200")
        window1.resizable(False, False) 
        blank1 = ttk.Label(window1, text = "    ", font=(None,15)) 
        label1 = ttk.Label(window1, text = "< 空氣品質檢測結果 >", font=(None,20)) 
        label2 = ttk.Label(window1, text = "空氣指數 : "+str(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
        label3 = ttk.Label(window1, text = "出遊建議 : "+grade(Quality(day1,day2,int(datehour.split("/")[-1]))), font=(None,15))
        button = ttk.Button(window1, text = "關閉", command = close)
        blank1.grid(row=0,column=0,pady=10)    
        label1.grid(row=0,column=1,pady=15)
        label2.grid(row=1,column=1,pady=10)
        label3.grid(row=2,column=1,pady=10)
        blank1.grid(row=3,column=0,pady=10)  
        button.grid(row=3,column=1,pady=10)

        window1.mainloop()
    except:
        global window3
        window3 = tk.Tk()
        window3.title("alert")
        window3.geometry("300x200")
        window3.resizable(False, False) 
        label = ttk.Label(window3, text = "    Please input the correct information",font=(None,15))
        label0 = ttk.Label(window3, text = "    Please check your internet",font=(None,15))
        button = ttk.Button(window3, text = "關閉", command = close)
        label.grid(pady=20)
        label0.grid(pady=20)
        button.grid(pady=20)
        window3.mainloop()

def graph():
    try:
        global mode
        mode = 0
        history_getdata()
        mode = 1
        index = kind_of_air(entry3.get())
        data = np.zeros(len(day1[index])-1, float)
        for i in range(1,len(day1[index])):
            if(type(day1[index][i])==float):
                data[i-1] = day1[index][i]
            else:
                data[i-1] = -1
        plt.title(entry3.get())
        plt.xlabel("hr")
        plt.ylabel(unit(entry3.get()))
        plt.plot(range(1,len(data)+1),data,"-o")
        plt.xticks(range(1,len(data)+1))
        plt.show()    
    except:
        global window3
        window3 = tk.Tk()
        window3.title("alert")
        window3.geometry("300x200")
        window3.resizable(False, False) 
        label = ttk.Label(window3, text = "   Please input the correct information",font=(None,15))
        label0 = ttk.Label(window3, text = "   Please check your internet",font=(None,15))
        button = ttk.Button(window3, text = "關閉", command = close)
        label.grid(pady=20)
        label0.grid(pady=20)
        button.grid(pady=20)
        window3.mainloop()

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
entryText1.set("XXXX/XX/XX/XX")#"XXXX/XX/XX/XX"

entryText2 = tk.StringVar()
entry2 = ttk.Entry(window, textvariable=entryText2, font=(None,15)) 
entryText2.set("Input the city")#"Input the city"

entryText3 = tk.StringVar()
entry3 = ttk.Entry(window, textvariable=entryText3, font=(None,15)) 
entryText3.set("Input the air parameter")#"Input the air parameter"

botton1 = ttk.Button(window, text = "即時空氣品質", width=20, command = instant_getdata)
botton2 = ttk.Button(window, text = "過去空氣品質", width=20, command = history_getdata)
botton3 = ttk.Button(window, text = "顯示數據圖", width=20, command = graph)

label0.grid(row=1, column=1, padx=15, pady=15)
label1.grid(row=2, column=0, padx=15, pady=15)
entry1.grid(row=2, column=1, padx=15, pady=15, ipady=5, ipadx=80)
botton1.grid(row=2, column=2, padx=15, pady=15, ipady=3, ipadx=3)
label2.grid(row=3, column=0, padx=15, pady=15)
entry2.grid(row=3, column=1, padx=15, pady=15, ipady=5, ipadx=80)
botton2.grid(row=3, column=2, padx=15, pady=15, ipady=3, ipadx=3)
label3.grid(row=4, column=0, padx=15, pady=15)
entry3.grid(row=4, column=1, padx=15, pady=15, ipady=5, ipadx=80)
botton3.grid(row=4, column=2, padx=15, pady=15, ipady=3, ipadx=3)
window.mainloop()



