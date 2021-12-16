from Data_Reader import data_reader

if __name__ == "__main__":

    path = "./Scaphoid/"
    data_reader_fcn = data_reader(path)
    data_reader_fcn.read_data()