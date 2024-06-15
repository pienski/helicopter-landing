import numpy as np

class Helicopter:
    def __init__(self, heliport, sd_distance, sd_angle):
        # Max size for x and y
        x_max = heliport.size_x / 2
        y_max = heliport.size_y / 2

        # Starting points should be higher that (-5, 5)
        x_rand = np.random.uniform(5, x_max)
        y_rand = np.random.uniform(5, y_max)

        self.x = np.random.choice([-1, 1]) * x_rand
        self.y = np.random.choice([-1, 1]) * y_rand

        self.z = heliport.size_z
        self.theta = np.random.uniform(0, 2*np.pi)
        self.sd_distance = sd_distance
        self.sd_angle = sd_angle

        self.actual = [] # Array for storing actual x, y, theta values in time
        self.starting_point = [self.x, self.y, self.z] # Coordinates of the starting point

    # Set parameters manually
    def set_parameters(self, pos_x, pos_y, pos_z, pos_theta, sd_distance, sd_angle):
        self.x = pos_x
        self.y = pos_y
        self.z = pos_z
        self.theta = pos_theta
        self.sd_distance = sd_distance
        self.sd_angle = sd_angle

    def move(self, desired_distance, desired_rotation):
        # Add noise to the movement
        distance_driven = np.random.normal(desired_distance, self.sd_distance)
        angle_rotated = np.random.normal(desired_rotation, self.sd_angle)
        
        # Update helicopter pose
        self.theta += angle_rotated
        self.theta = np.mod(self.theta, 2*np.pi) # Angles between [0, 2*pi]

        self.x += distance_driven * np.cos(self.theta)
        self.y += distance_driven * np.sin(self.theta)

        # Store actual position in time
        self.actual.append(self.get_actual_position())

    def get_actual_position(self):
        return [self.x, self.y, self.theta]
    
    def measure(self):
        # Measure current state of x, y, theta - with noise
        x = np.random.normal(self.x, self.sd_distance, 1)[0]
        y = np.random.normal(self.y, self.sd_distance, 1)[0]
        theta = np.random.normal(self.theta, self.sd_angle, 1)[0]
        return [x, y, theta]
    
    def measure_00(self, x, y):
        # Measure distance and angle to point (0,0) - with noise
        distance = np.random.normal(np.sqrt(x * x + y * y), self.sd_distance)
        angle = np.random.normal(np.arctan2(-y, -x), self.sd_angle)
        # Show as the angle between the point (x,y) in relation to (0,0)
        angle = np.mod(angle - 2*np.pi, 2*np.pi)
        return [distance, angle]

    def measure_lm(self, heliport):
        # Measure distance fromn helicopter to landmarks - with noise
        measurements = []
        for lm in heliport.landmarks:
            dx = self.x - lm[0]
            dy = self.y - lm[1]

            # Measured distance perturbed by zero mean additive Gaussian noise
            z_distance = np.random.normal(np.sqrt(dx * dx + dy * dy), self.sd_distance)

            # Measured angle perturbed by zero mean additive Gaussian noise
            z_angle = np.random.normal(np.arctan2(dy, dx), self.sd_angle)

            # Store measurement
            measurements.append([z_distance, z_angle])

        return measurements
    
    def get_00_dt(self, coordinates):
        # Get real distance to point 00, without any noise
        x = coordinates[0]
        y = coordinates[1]
        distance = np.sqrt(x * x + y * y)
        return distance