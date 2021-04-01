import softmaxBandit
import matplotlib.pylab as plt

result_1 = softmaxBandit.run(3, 0.1, 100000, False)
result_05 = softmaxBandit.run(3, 0.05, 100000, False)
result_01 = softmaxBandit.run(3, 0.01, 100000, False)

# log scale plot
plt.title("epsilon greedy (log scale plot)")
plt.plot(result_1, label = "eps = 0.10")
plt.plot(result_05, label = "eps = 0.05")
plt.plot(result_01, label = "eps = 0.01")
plt.legend()
plt.xscale("log")
plt.show()

# linear plot
plt.title("epsilon greedy (linear plot)")
plt.plot(result_1, label = "eps = 0.10")
plt.plot(result_05, label = "eps = 0.05")
plt.plot(result_01, label = "eps = 0.01")
plt.legend()
plt.show()