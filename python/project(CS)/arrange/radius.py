import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from copy import copy
from find import find, trace, take_line
from filters import Sobelfilter, bfsfilter, Cannyedge
import pickle
import os
import warnings
warnings.filterwarnings("ignore")

#diraction step
dirac=[[1,0],[0,1],[1,1],[1,-1]]

#show
def showCV(title,image):
    cv2.imshow(title,image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def draw_circles(todraw,all_x_y_r,color,need_center=True,draw_in_copy=False):
    if draw_in_copy:    to_draw=copy(todraw)
    else:   to_draw=todraw
    for i in all_x_y_r:
        #cv2.circle(to_draw,(i[0],i[1]),i[2],color,2) # draw the outer circle
        if need_center:
            cv2.circle(to_draw,(i[0],i[1]),2,color,3) # draw the center of the circle
    return to_draw

#dealing graph
def clear_white_edge(graph,white):
    white_line_wide=0
    m=len(graph)
    n=len(graph[0])
    
    def judge(value,white):
        if type(white)==int:
            if value==white:
                return True
            else:
                return False
        else:
            tf=False
            for i in range(len(white)):
                if value[i]==white[i]:
                    return True
            return False
    
    for j in range(n):
        i=0
        while i <m:
            if not judge(graph[i][j],white):
                break
            i+=1
        if i<m:
            break
        white_line_wide+=1
    return np.array([[graph[i][j] for j in range(white_line_wide,n)] for i in range(m)],np.uint8)

def Radiuscal(todraw,bright,center,Pixellength,visible=False):
    all_Radius = [[], []]

    init = 0
    InRadius , OutRadius = 0 , 0
    in_Radius = [[] for i in range(4)]
    out_Radius = [[] for i in range(4)]
    for index in range(len(bright)):
        start_offset=-int(center[index])
        ending=len(bright[index])+start_offset
        cv2.line(todraw,(center[0]+start_offset*dirac[index][0],center[1]+start_offset*dirac[index][1]),(center[0]+ending*dirac[index][0],center[1]+ending*dirac[index][1]),(255,255,255),2)
        
        r = np.linspace(0,Pixellength*len(bright[index]),len(bright[index]))
                
        tmp = trace(bright[index],center[index])
        min_center = tmp[1],bright[index][tmp[1]]
        max_left = tmp[0],bright[index][tmp[0]]
        max_right = tmp[2],bright[index][tmp[2]]

        in_height = np.mean([min_center[1],min_center[1],max_right[1],max_left[1]])
        out_height = np.mean([init,init,max_right[1],max_left[1]])
        
        for i in range(len(bright[index])-1):
            if((bright[index][i]-in_height)*(bright[index][i+1]-in_height)<=0 and i>=max_left[0] and i<=max_right[0]):
                in_Radius[index].append(i)
                cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
            
            elif(i==min_center[0]):
                in_Radius[index].append(i)
                #cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
                                        
            if((bright[index][i]-out_height)*(bright[index][i+1]-out_height)<=0):
                out_Radius[index].append(i)
                
            elif(i==min_center[0]):
                out_Radius[index].append(i)
                #cv2.circle(todraw,(center[0]+(start_offset+i)*dirac[index][0],center[1]+(start_offset+i)*dirac[index][1]),2,(0,0,255),3)
        # print(in_Radius)
        # print(out_Radius)       
        ans = [in_Radius[index][in_Radius[index].index(min_center[0])-1],in_Radius[index][in_Radius[index].index(min_center[0])+1]]
        for i in range(len(out_Radius[index])):
            if(out_Radius[index][i]>=ans[0]):
                ans.append(out_Radius[index][i-1])
                cv2.circle(todraw,(center[0]+(start_offset+ans[len(ans)-1])*dirac[index][0],center[1]+(start_offset+ans[len(ans)-1])*dirac[index][1]),2,(0,0,255),3)
                break
        
        for j in range(i,len(out_Radius[index])):
            if(out_Radius[index][j]>ans[1]):
                ans.append(out_Radius[index][j])
                cv2.circle(todraw,(center[0]+(start_offset+ans[len(ans)-1])*dirac[index][0],center[1]+(start_offset+ans[len(ans)-1])*dirac[index][1]),2,(0,0,255),3)
                break
        #print(ans)
        if(index==2 or index==3):
            c = (2)**0.5
        else:
            c = 1
        r = c*r
        h = Pixellength
        all_Radius[0].append(c*(ans[1]-ans[0])*h)
        all_Radius[1].append(c*(ans[3]-ans[2])*h)
        InRadius , OutRadius = InRadius+c*(ans[1]-ans[0])*h/4 ,  OutRadius+c*(ans[3]-ans[2])*h/4

        if(visible):
            print("\nMin pos and value:\n   ", end="")
            print(r[min_center[0]],min_center[1])
            print("Max-right pos and value:\n   ", end="")
            print(r[max_right[0]],max_right[1])
            print("Max-left pos and value:\n   ", end="")
            print(r[max_left[0]],max_left[1])
            plt.subplot(221+index)
            plt.scatter([init,r[min_center[0]],r[max_right[0]],r[max_left[0]]],[init,min_center[1],max_right[1],max_left[1]],color = "r")
            plt.title("Calculate Bright")
            plt.xlabel("width (\u03BCm)")
            plt.ylabel("brightness")
            plt.plot([r[ans[0]],r[ans[1]]],[in_height,in_height],"-o",label = "in")
            plt.plot([r[ans[2]],r[ans[3]]],[out_height,out_height],"-o",label = "out")
            plt.plot(r,bright[index])
            plt.legend()
            
    if(visible):
        plt.tight_layout() 
        plt.show()
        plt.clf()
        showCV('hey',todraw)

    return InRadius, OutRadius, todraw, all_Radius

def Total_Radius(name, length, filter_mode, checkbox, visible):
#-#-#-#-#-#-#-#-#main------------------------------------------
    rgb=clear_white_edge(cv2.imread(name),(255,255,255))
    Ogray=clear_white_edge(cv2.imread(name,0),255)
    gray=copy(Ogray)

    #length, hight about values===================================
    m=len(gray)
    n=len(gray[0])
    Pixellength = length/n
    Rrange=[10,40]
    Range=[[0,n-1],[0,m-1]]

    #operating_graph
    todraw=copy(rgb)

    try:
        os.mkdir(str(name.split(".")[0]) + "_" + filter_mode)
    except:
        pass

    path = "./{}/".format(name.split(".")[0] + "_" + filter_mode)

    #############################################################
    data = set(glob(path + "*.pickle"))
    if(filter_mode == "bfsfilter"):
        if(path + "onebit.pickle" not in data or path + "continents.pickle" not in data or path + "grays.pickle" not in data):
            onebit,continents,grays=bfsfilter(gray, Rrange)
            p_w=open(path + "onebit.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
            pickle.dump(onebit,p_w) #將li 寫入p_w
            p_w.close() #關閉
            p_w=open(path + "continents.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
            pickle.dump(continents,p_w) #將li 寫入p_w
            p_w.close() #關閉
            p_w=open(path + "grays.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
            pickle.dump(grays,p_w) #將li 寫入p_w
            p_w.close() #關閉
        else:
            p_r=open(path + "onebit.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
            onebit=pickle.load(p_r)    #讀取p_r之內容
            p_r.close() #關閉
            p_r=open(path + "continents.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
            continents=pickle.load(p_r)    #讀取p_r之內容
            p_r.close() #關閉
            p_r=open(path + "grays.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
            grays=pickle.load(p_r)    #讀取p_r之內容
            p_r.close() #關閉
        length = len(continents)

        if(visible):
            showCV("pp",onebit)
    else:
        if(filter_mode == "Sobelfilter"):
            edge = Sobelfilter(gray)
        elif(filter_mode == "Cannyedge"):
            edge = Cannyedge(gray)
        else:
            print("Please choose the correct filter !!!")
        onebit = cv2.inRange(gray,90,130)
        circles=cv2.HoughCircles(edge,cv2.HOUGH_GRADIENT,1,80,param1=10,param2=30,minRadius=Rrange[0],maxRadius=Rrange[1])[0]
        length = len(circles)
    #mark=np.zeros([len(onebit),len(onebit[0])],bool)  #好像用不到

    inRadius=[]
    outRadius=[]
    index = 1
    Radius_data = {}
    for i in range(length):
        try:
            if(filter_mode == "bfsfilter"):
                gray = grays[i] # one_blood_gray
                onebit = continents[i][0] # one_blood_onebit
                edge = cv2.Canny(onebit, 1, 1) 
                circles = cv2.HoughCircles(edge,cv2.HOUGH_GRADIENT,1,1000,param1=10,param2=1,minRadius=Rrange[0],maxRadius=Rrange[1])
                circle = np.uint16(np.around(circles[0]))
            elif(filter_mode == "Sobelfilter" or filter_mode == "Cannyedge"):
                gray = gray #數值已固定
                onebit = onebit #數值已固定
                edge = edge #數值已固定
                circles = circles #數值已固定
                circle = [np.uint16(np.around(circles[i]))]
            else:
                print("Please choose the correct filter !!!")
                break
            if(checkbox["Center"]):
                xx = find(onebit, circle[0][:2])
            else:
                xx = circle[0][:2]
            lines,centerI = take_line(gray, xx)
            in_r, out_r, drawtmp, all_Radius = Radiuscal(copy(todraw), lines, centerI, Pixellength, visible)
            inRadius.append(in_r)
            outRadius.append(out_r)
            cv2.imwrite(path + str(index) + ".png", drawtmp)
            print(path + str(index) + ".png")
            if(checkbox["Report"]):
                f = open(path + "Report.txt", "a")
                f.write(path + str(index) + ".png")
                f.write("\n")
                f.write("in_Radius : " + str(all_Radius[0]))
                f.write(" average : " + str(in_r))
                f.write("\n")
                f.write("out_Radius : " + str(all_Radius[1]))
                f.write(" average : " + str(out_r))
                f.write("\n\n")
                f.close()
            Radius_data[path + str(index) + ".png"] = [in_r, out_r]
            index += 1
        except:
            plt.clf()
    #===================
    if(checkbox["Report"]):
        f = open(path + "Report.txt", "a")
        f.write("Total averge : ")
        f.write("\n")
        f.write("in_Radius : " + str(np.average(inRadius)))
        f.write("\n")
        f.write("out_Radius : " + str(np.average(outRadius)))
        f.write("\n")
        f.close()
        
    # print(inRadius)
    # print(outRadius)
    return inRadius, outRadius, Radius_data

if __name__ == "__main__":
    #all kinds of images we need======================
    #base_graph,
    name="multibad3.bmp"
    name="multigood1.bmp"

    filter_mode = "Sobelfilter"
    filter_mode = "Cannyedge"
    #filter_mode = "bfsfilter"
    checkbox = {"Center":True, "Report":True, "None":True}
    print(Total_Radius(name, 50, filter_mode, checkbox, True))



