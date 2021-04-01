import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

class Bandit:
    def __init__(self, m):
        self.machine = m
        self.mean = 0
        self.N = 0

    def reward(self):
        return self.machine + np.random.randn() # noise

    def update(self, new_value):
        self.N += 1
        self.mean = ((self.N - 1) * self.mean + new_value) / self.N # 更新平均值

def Probability_Distribution(bandits): # 為softmax的分布

    probability_space = 0
    probability_sample = np.zeros(len(bandits))

    for i in range(len(bandits)):
        probability_sample[i] = np.e ** (bandits[i].machine)
        probability_space += probability_sample[i]

    return probability_sample / probability_space

def run(number_of_machine, epsilon, N, visiable = True):
    machines = np.arange(1, number_of_machine + 1, 1)
    bandits = [Bandit(m) for m in machines]
    probability_distribution = Probability_Distribution(bandits)

    each_step_reward = np.empty(N)

    for step in range(N):
        # softmax algorithms
        probability = np.random.random()
        if probability < epsilon:
            choose = np.random.choice(number_of_machine, p = probability_distribution)
        else:
            bandits_mean = [bandit.mean for bandit in bandits]
            choose = np.random.choice(np.where(bandits_mean == np.max(bandits_mean))[0]) # 若出現相同應該隨機選擇

        reward = bandits[choose].reward()
        bandits[choose].update(reward)
        each_step_reward[step] = reward

    cumulative_average = np.cumsum(each_step_reward) / (np.arange(N) + 1)

    # plot moving average ctr
    if visiable:
        for m in machines:
            plt.plot(np.ones(N) * m)
        plt.plot(cumulative_average)
        plt.xscale("log")
        plt.show()

    return cumulative_average

if __name__ == "__main__":
    result_1 = run(3, 0.1, 100000)
    result_05 = run(3, 0.05, 100000)
    result_01 = run(3, 0.01, 100000)

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

