# This is Abao's code

import re

def expand(s):
    s = re.split('{|}',s.strip('{}'))
    capacity = []
    content = []
    count = []
    for i in s:
        tmp = i.split(",")
        content.append(tmp)
        capacity.append(len(tmp))
        count.append(0)
    ans = []
    flag=1
    while flag==1:
        tmp = ""
        for i in range(len(content)):
            tmp += content[i][count[i]]
        ans.append(tmp)
        count[-1] += 1
        for i in range(len(count)-1,0,-1):
            if(count[i]==capacity[i]):
                count[i] = 0
                count[i-1] += 1
        flag=0
        for i in range(len(count)):
            if(count[i]+1!=capacity[i]):
                flag=1
                break
    tmp = ""
    for i in range(len(content)):
        tmp += content[i][capacity[i]-1]
    ans.append(tmp)
    return ans

inp = "{a,b,c}d{e,f}"
print(expand(inp))


    


    