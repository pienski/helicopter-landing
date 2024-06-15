import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KernelDensity

class Presentation:

    def __init__(self, heliport):
        self.x_margin = heliport.size_x / 2
        self.y_margin = heliport.size_y / 2
        self.landmarks = heliport.landmarks

    # 2D visualisation of the process
    def visualise(self, particles, helicopter):        

        # Clear the previous plot
        plt.clf()

        # Dimensions of plot
        x_min = -self.x_margin
        x_max = self.x_margin
        y_min = -self.y_margin
        y_max = self.y_margin

        # Add particles
        x_particles = particles[:, 0]
        y_particles = particles[:, 1]
        plt.scatter(x_particles, y_particles, color='blue')

        # Add landmarks
        x_lms = [coord[0] for coord in self.landmarks]
        y_lms = [coord[1] for coord in self.landmarks]
        plt.scatter(x_lms, y_lms, color='green', linewidth=2)

        # Real postion of the helicopter
        r_position = helicopter.get_actual_position()
        r_x = r_position[0]
        r_y = r_position[1]
        r_angle = r_position[2]
        plt.scatter(r_x, r_y, color='red')
        r_dx = np.cos(r_angle)
        r_dy = np.sin(r_angle)
        plt.arrow(r_x, r_y, r_dx, r_dy, head_width=0.5, head_length=0.5, fc='red', ec='red')

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xlabel('X Coordinates')
        plt.ylabel('Y Coordinates')
        plt.title('Helicopter landing')
        plt.grid(True)

        # Show
        plt.draw()
        plt.pause(0.05)

    def plot_pdf(self, particles, state_variable):

        # Extract the state variable index based on the input
        variable_index = {'x': 0, 'y': 1, 'theta': 2}[state_variable]

        # Extract the state values and weights from the particles
        state_values = particles[:, variable_index].reshape(-1, 1)
        weights = particles[:, -1]

        # Create an instance of the KernelDensity estimator
        kde = KernelDensity(bandwidth=0.75, kernel='gaussian')

        # Fit the KDE model to the state values
        kde.fit(state_values, sample_weight=weights)

        # Generate points on the x-axis for plotting
        x_plot = np.linspace(state_values.min() - 1, state_values.max() + 1, 1000).reshape(-1, 1)

        # Compute the estimated density for the generated points
        log_density = kde.score_samples(x_plot)

        # Plot the KDE estimate
        plt.plot(x_plot, np.exp(log_density), label='KDE estimate')
        plt.scatter(state_values, np.zeros_like(state_values), alpha=0.5, label='Particles')

        plt.xlabel(f'State {state_variable}')
        plt.ylabel('Density')
        plt.title(f'Kernel Density Estimation for State {state_variable}')
        
        plt.draw()
        plt.pause(0.05)