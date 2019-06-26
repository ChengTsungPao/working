from visual import *              
from visual . graph import *
import random
import sys
from types import *
from time import clock , time         #import需要用到的library

trials = 100                          #骰子試驗的次數
print "Number of trials = ", trials   #印出骰子試驗的次數
sides = 6                             #骰子總共有六面

histogram = zeros(sides , int)        #利用陣列初始化骰子各點分布的次數[0,0,0,0,0,0]
print histogram                       #印出初始化骰子的陣列
sum = 0.0                             
j=0
r=0
while j < trials :                    #利用迴圈控制試驗次數
    r=int(random.random()*sides)      #隨機從1~sides中選一個當作此次試驗的結果(程式事實上為:0~sides-1)
    histogram[r] = histogram[r] + 1   #將被選中的試驗結果+1
    j=j+1                             #將目前已試驗的次數+1
j=0
while j < sides :                     #利用迴圈印出各情況分布(histogram[j])和各情況的離差(histogram[j]-trials/sides)
    print histogram[j], histogram[j]-trials/sides 
    j=j+1

