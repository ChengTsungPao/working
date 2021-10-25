
def getParameter(light, imageType):
    
    tableL = {
        "light": "Binary",
            30 :  35 ,
            50 :  80 ,
           100 : 110 ,
           150 : 155 ,
           200 : 200 ,
           255 : 245
    }

    tableR = {
        "light": "Binary",
            30 :  27 ,
            50 :  40 ,
           100 : 102 ,
           150 : 147 ,
           200 : 192 ,
           255 : 245
    }

    if imageType == "L":
        return tableL[light]
    else:
        return tableR[light] 
