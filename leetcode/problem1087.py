# This is Abao's code

import re
import numpy as np

class Solution:
    def expand(self,S: str):
        s = re.split('}{|{|}',S.strip('{}'))        
        content = []
        capacity = np.zeros(len(s),int)
        count = np.zeros(len(s),int)
        for i in range(len(s)):
            tmp = sorted(s[i].split(","))
            content.append(tmp)
            capacity[i] = len(tmp)-1

        ans = []
        while (count!=capacity).any():
            tmp = ""
            for i in range(len(content)):
                tmp += content[i][count[i]]
            ans.append(tmp)
            count[-1] += 1
            for i in range(len(count)-1,0,-1):
                if(count[i]==capacity[i]+1):
                    count[i] = 0
                    count[i-1] += 1

        tmp = ""
        for i in range(len(content)):
            tmp += content[i][capacity[i]]
        ans.append(tmp)
        return ans

inp = "{a,b,c}d{e,f}"
fcn = Solution()
print(fcn.expand(inp))


    


    