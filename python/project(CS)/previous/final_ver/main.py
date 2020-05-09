import os
import pickle
from time import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

from filters import BFSfilter,clear_white_edge,cell_cut,cut_graph
from draw_and_show import showCV
from rad_cal import find,take_line,trace,Circle,Radiuscal

thresh=20
if __name__=='__main__':
    path=''#r"C:\CodingWorkSpace\blood\newnew\tide\datas\erythrocyte"
    bmp=".bmp"
    file="bad1.bmp"
    #file=health+str(wi+1)+bmp
    print(os.path.join(path,file))
    rgb=clear_white_edge(cv2.imread(os.path.join(path,file)),(255,255,255))
    Ogray=clear_white_edge(cv2.imread(os.path.join(path,file),0),255)
    gray=copy(Ogray)
    
    t=time()
    onebit,continents,gray=BFSfilter(gray,thresh)    
    t=time()-t
    print(t)
    
    
    p_w=open("onebit.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
    pickle.dump(onebit,p_w) #將li 寫入p_w
    p_w.close() #關閉
    p_w=open("continents.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
    pickle.dump(continents,p_w) #將li 寫入p_w
    p_w.close() #關閉
    p_w=open("grays.pickle",'wb')    #新建或開啟 pickle檔案為寫入模式，紀錄於p_w
    pickle.dump(grays,p_w) #將li 寫入p_w
    p_w.close() #關閉
    
    
    
    p_r=open("onebit.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
    onebit=pickle.load(p_r)    #讀取p_r之內容
    p_r.close() #關閉
    p_r=open("continents.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
    continents=pickle.load(p_r)    #讀取p_r之內容
    p_r.close() #關閉
    p_r=open("grays.pickle",'rb')    #開啟 pickle檔案為讀取模式，紀錄於p_r
    grays=pickle.load(p_r)    #讀取p_r之內容
    p_r.close() #關閉
    
    showCV(onebit)
