from Music_Genre_Dataset import music_genre_dataset
from Music_Genre_Train import music_genre_train

if __name__ == "__main__":
    kind = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]

    path = "./dataset"
    # dataset = music_genre_dataset(path)
    # dataset.plotOriginData(kind[1], 0)
    # dataset.plotFFTData(kind[1], 0)

    music_genre_train_func = music_genre_train(path)
    music_genre_train_func.train_origin()



