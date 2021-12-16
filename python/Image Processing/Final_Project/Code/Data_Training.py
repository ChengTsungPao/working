from Data_Transfer import data_transfer

class data_training(data_transfer):

    def __init__(self, path):
        super().__init__(path)


    def setupData(self):
        self.read_data()


    def train_bounding_box_wider_data(self):
        pass
