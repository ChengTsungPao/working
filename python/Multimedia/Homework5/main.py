from Music_Genre_Dataset import music_genre_dataset
from Music_Genre_Train import music_genre_train

if __name__ == "__main__":

    path = "./dataset"
    # dataset = music_genre_dataset(path)
    # dataset.plotOriginData()
    # dataset.plotFFTData()
    # dataset.plotSpectogramData()

    music_genre_train_func = music_genre_train(path)
    music_genre_train_func.train(2)

    # filename = "2022_0507_0012_Origin"
    # filename = "2022_0506_1819_FFT"
    # filename = "2022_0506_0545_Spectrogram"
    # music_genre_train_func.predict(filename)
    # music_genre_train_func.plotResult(filename)