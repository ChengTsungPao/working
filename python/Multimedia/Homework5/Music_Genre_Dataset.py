import numpy as np
from glob import glob
from scipy.fft import fft
from scipy.io.wavfile import read
import matplotlib.pylab as plt


class music_genre_dataset:
    def __init__(self, path):
        self.path = path
        self.kind = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

        self.datas = []
        self.labels = []
        self.FFTDatas = []

    def readOriginData(self):
        for i, k in enumerate(self.kind):

            for p in glob("{}/{}/*.wav".format(self.path, k)):
                _, data = read(p)
                self.datas.append(data.copy()[:65000])
                self.labels.append(i)

        self.datas = np.array(self.datas, float)
        self.labels = np.array(self.labels)

    def transferFFTData(self):
        if self.datas == []:
            self.readOriginData()

        for data in self.datas:
            self.FFTDatas.append(fft(data))

        self.FFTDatas = np.array(self.FFTDatas)

    def plotOriginData(self, kind = "blues", index = 0):
        paths = glob("{}/{}/*.wav".format(self.path, kind))
        _, data = read(paths[index])

        plt.title("{} (index = {})".format(kind, index))
        plt.plot(data)
        plt.show()

    def plotFFTData(self, kind = "blues", index = 0):
        paths = glob("{}/{}/*.wav".format(self.path, kind))
        _, data = read(paths[index])

        plt.title("{} (index = {})".format(kind, index))
        plt.plot(fft(data))
        plt.show()

        