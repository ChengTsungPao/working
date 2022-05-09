import librosa
import numpy as np
from glob import glob
from scipy.fft import fft, dct
from scipy.io.wavfile import read
import matplotlib.pylab as plt


class music_genre_dataset:
    def __init__(self, path):
        self.path = path
        self.kind = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

        self.datas = []
        self.labels = []
        self.FFTDatas = []
        self.SpectrogramDatas = []

    def readOriginData(self):
        for i, k in enumerate(self.kind):

            for p in glob("{}/{}/*.wav".format(self.path, k)):
                _, data = read(p)
                self.datas.append(np.resize(data, 67000))
                self.labels.append(i)

        self.datas = np.array(self.datas, float)
        self.labels = np.array(self.labels)

    def transferFFTData(self):
        if self.datas == []:
            self.readOriginData()

        for data in self.datas:
            self.FFTDatas.append(fft(np.resize(data, 67000)).real)

        self.FFTDatas = np.array(self.FFTDatas)

    def transferSpectrogramData(self):
        if self.datas == []:
            self.readOriginData()

        for k in self.kind:

            for p in glob("{}/{}/*.wav".format(self.path, k)):
                y , sr = librosa.load(p, mono=True, duration=30)
                spectogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, n_fft=2048, hop_length=1024)
                spectogram = librosa.power_to_db(spectogram, ref=np.max)
                self.SpectrogramDatas.append(np.resize(spectogram, (128, 512)))

        self.SpectrogramDatas = np.array(self.SpectrogramDatas)

    def plotOriginData(self, kindIndex = 0, index = 0):
        paths = glob("{}/{}/*.wav".format(self.path, self.kind[kindIndex]))
        _, data = read(paths[index])

        plt.title("{} (index = {})".format(self.kind[kindIndex], index))
        plt.plot(data)
        plt.show()

    def plotFFTData(self, kindIndex = 0, index = 0):
        paths = glob("{}/{}/*.wav".format(self.path, self.kind[kindIndex]))
        _, data = read(paths[index])

        plt.title("{} (index = {})".format(self.kind[kindIndex], index))
        plt.plot(fft(data))
        plt.show()

    def plotSpectogramData(self, kindIndex = 0, index = 0):
        paths = glob("{}/{}/*.wav".format(self.path, self.kind[kindIndex]))

        y , sr = librosa.load(paths[index], mono=True, duration=30)
        spectogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, n_fft=2048, hop_length=1024)
        spectogram = librosa.power_to_db(spectogram, ref=np.max)

        plt.title("{} (index = {})".format(self.kind[kindIndex], index))
        plt.imshow(spectogram, origin="lower", cmap=plt.get_cmap('inferno'))
        plt.show()