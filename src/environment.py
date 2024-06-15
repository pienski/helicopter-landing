import numpy as np
class Heliport:
    def __init__(self, number_of_landmarks):
        # Initialize a heliport with random values of parameters
        size_constraints = [15, 30]
        random_size = np.random.randint(size_constraints[0], size_constraints[1], 1)
        self.size_x = random_size[0]
        self.size_y = random_size[0]
        self.size_z = random_size[0]
        range_x = self.size_x / 2
        range_y = self.size_y / 2
        # Choose n random landmark coordinates
        self.landmarks = [
            [np.random.uniform(-range_x, range_x, 1)[0], np.random.uniform(-range_y, range_y, 1)[0]]
            for i in range(number_of_landmarks)
        ]

    # Set parameters manually
    def set_parameters(self, size_x, size_y, size_z, landmarks):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.landmarks = landmarks