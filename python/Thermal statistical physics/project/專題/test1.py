import matplotlib.pyplot as plt


data = [0,0,24,6,0]
plt.title("Air quality")
plt.xlabel("risk rank")
plt.ylabel("days")
plt.bar(range(1,len(data)+1),data,color = "gbbr")
plt.show()
