import epsilonGreedyBandit
import matplotlib.pylab as plt

result_0 = epsilonGreedyBandit.run(3, 0, 100000, False) # greedy algorithms
result_1 = epsilonGreedyBandit.run(3, 0.1, 100000, False)
result_05 = epsilonGreedyBandit.run(3, 0.05, 100000, False)
result_01 = epsilonGreedyBandit.run(3, 0.01, 100000, False)

# log scale plot
plt.title("epsilon greedy (log scale plot)")
plt.plot(result_0, label = "eps = 0.00 (greedy)")
plt.plot(result_1, label = "eps = 0.10")
plt.plot(result_05, label = "eps = 0.05")
plt.plot(result_01, label = "eps = 0.01")
plt.legend()
plt.xscale("log")
plt.show()

# linear plot
plt.title("epsilon greedy (linear plot)")
plt.plot(result_0, label = "eps = 0.00 (greedy)")
plt.plot(result_1, label = "eps = 0.10")
plt.plot(result_05, label = "eps = 0.05")
plt.plot(result_01, label = "eps = 0.01")
plt.legend()
plt.show()