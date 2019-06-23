import numpy as np
import matplotlib.pylab as plt
import copy

#wh = "高雄"
#air = "CO"
def analysis(wh, air):

    f = open("./data/"+wh+"/"+wh+air+".txt",'r')
    line = f.readline()
    print(wh)
    print(air)
    data = []
    while line:
        try:
            if(int(line[0])==0 or int(line[0])==1):
                #print(line) 
                tmp = line.split(" ")
                for i in range(1,len(tmp)):
                    try:
                        if(float(tmp[i])!=0): data.append(float(tmp[i]))
                    except:
                        pass
        except:
            a = 1
        line = f.readline()

    #print(data)


    tmp = 1
    status = np.zeros(10, int)
    temp = 0
    for i in range(len(data)-1):
        #print(abs((data[i+1]-data[temp])*100/data[temp]))
        
        try:
            if(abs((data[i+1]-data[temp])*100/data[temp])<50):
                tmp += 1 
            else:
                if(tmp >= len(status)):
                    s = np.zeros(tmp+1, int)
                    for i in range(len(status)):
                        s[i] = status[i]
                    status = copy.copy(s)
                #print(len(status))
                #print(tmp)
                status[tmp] += 1
                temp = i+1
                tmp = 1
        except:
            pass


    print(status)

    times = 0
    sum = 0
    for i in range(len(status)):
        sum += i*status[i]
        times += status[i]
    print(sum/times)

    mid = 0
    for i in range(len(status)):
        mid += status[i]
        if(mid > times/2):
            break
    print(i)


    plt.plot(range(len(status)),status)
    plt.show()


wh = ["台北","新北","桃園","新竹","苗栗","台中","彰化","雲林","嘉義",
      "台南","高雄","屏東","台東","花蓮","宜蘭","澎湖","基隆","南投"]

air = ["PM10","SO2","CO","O3","NO2"]
air = ["NO2"]
for j in air:
    for i in wh:    
        analysis(i,j)













