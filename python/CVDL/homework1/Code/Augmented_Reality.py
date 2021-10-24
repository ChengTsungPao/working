from Corner_Detection import corner_detection


class augmented_reality(corner_detection):
    def __init__(self, path):
        super().__init__(path)
        self.find_intrinsic()
        extrinsic = self.find_extrinsic(1)