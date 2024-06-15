import numpy as np
import copy

class ParticleFilter:
    def __init__(self, num_particles, size, sd_distance, sd_angle):
        self.num_particles = num_particles
        self.size_x = size[0]
        self.size_y = size[1]
        self.sd_distance = sd_distance # Standard deviation of noise in distance
        self.sd_angle = sd_angle # Standard deviation of noise in angle
        self.predicted = [] # Array for storing predicted x, y, theta values in time

    def initialize_particles(self):
        # 4 variables: x, y, theta, weigth
        particles = np.empty((self.num_particles, 4))
        range_x = self.size_x / 2
        range_y = self.size_y / 2
        particles[:, 0] = np.random.uniform(-range_x, range_x, size=self.num_particles)
        particles[:, 1] = np.random.uniform(-range_y, range_y, size=self.num_particles)
        particles[:, 2] = np.random.uniform(0, np.pi*2, size=self.num_particles) #in radians
        particles[:, 3] = 1.0 / self.num_particles
        return particles

    def update_particles(self, particles, forward_dt, rotation):
        # Update particle positions based on the movement of the helicopter
        updated_particles = copy.deepcopy(particles)
        for particle in updated_particles:
            # 1. rotate the helicopter
            particle[2] += np.random.normal(rotation, self.sd_angle, 1)
            # 2. add noise to forward movement
            forward_dt_noise = np.random.normal(forward_dt, self.sd_distance, 1)
            # 3. move forward
            particle[0] += forward_dt_noise * np.cos(particle[2])
            particle[1] += forward_dt_noise * np.sin(particle[2])
        return updated_particles
    
    # Compute likelihood p(z|sample) for a specific measurement given current sample state and landmarks
    def compute_likelihood(self, particles, measurement, landmarks):

        # Initialize measurement likelihood
        updated_weights = copy.deepcopy(particles)

        for particle in updated_weights:
            likelihood_sample = 1.0
            # Angle must be in range [0, 2*pi]
            particle[2] = np.mod(particle[2], 2*np.pi)
            # Loop over all landmarks for current particle
            for i, lm in enumerate(landmarks):

                # Compute expected measurement assuming the current particle state
                dx = particle[0] - lm[0]
                dy = particle[1] - lm[1]
                expected_distance = np.sqrt(dx*dx + dy*dy)
                expected_angle = np.arctan2(dy, dx)

                dist_diff = expected_distance - measurement[i][0]
                angle_diff = expected_angle - measurement[i][1]

                # Incorporate likelihoods for current landmark
                likelihood_sample *= (1.0 / (np.sqrt(2 * np.pi) * 1.0)) * np.exp(-0.5 * (dist_diff**2 / 1.0**2))
                likelihood_sample *= (1.0 / (np.sqrt(2 * np.pi) * 1.0)) * np.exp(-0.5 * (angle_diff**2 / 1.0**2))
            
            particle[3] *= likelihood_sample

        return updated_weights

    def normalize_weights(self, particles):
        sum_weights = sum(particle[3] for particle in particles)
        for particle in particles:
            particle[3] = particle[3] / sum_weights
        return particles
    
    def systematic_resample(self, particles):
        N = self.num_particles
        Q = np.cumsum(particles[:, 3])

        # Draw one sample
        u0 = np.random.uniform(1e-10, 1.0 / N, 1)[0]

        # As long as the number of new samples is insufficient
        n = 0
        m = 0  # index first element
        new_samples = np.empty((N, 4))
        while n < N:

            # Compute u for current particle (deterministic given u0)
            u = u0 + float(n) / N

            # Get first sample for which cumulative sum is above u
            while Q[m] < u:
                m += 1

            # Add state sample (uniform weights)
            new_samples[n] = particles[m]

            # Added another sample
            n += 1

        # Return new samples
        new_samples[:, 3] = 1.0 / N
        return new_samples
    
    def multinomial_resampling(self, particles):
        Q = np.cumsum(np.array(particles)[:, 3])
        N = self.num_particles

        n = 0
        new_samples = np.empty((N, 4))
        while n < N:

            # Draw a random sample u
            u = np.random.uniform(1e-6, 1, 1)[0]

            # Naive search (alternative: binary search)
            m = self.naive_search(Q, u)

            # Add copy of the state sample (uniform weights)
            new_samples[n] = particles[m]

            # Added another sample
            n += 1

        new_samples[:, 3] = 1.0 / N
        return new_samples
    
    def estimate_state(self, particles):
        avg_x = 0.0
        avg_y = 0.0
        avg_theta = 0.0
        for particle in particles:
            avg_x += particle[3] * particle[0]
            avg_y += particle[3] * particle[1]
            avg_theta += particle[3] * particle[2]
        estimations = [avg_x, avg_y, avg_theta]
        # Store estimations
        self.predicted.append(estimations)
        return estimations

    @staticmethod
    def naive_search(cumulative_list, x):
        m = 0
        while cumulative_list[m] < x:
            m += 1
        return m