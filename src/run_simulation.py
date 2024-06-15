from environment import Heliport
from landing_simulator import Helicopter
from particle_filter import ParticleFilter
from presentation import Presentation

def run_simulation(number_of_particles, number_of_landmarks, sd_distance, sd_angle, plot_type, pdf_variable, resampling_method, print_results=True):

    # Instantiate heliport
    heliport = Heliport(number_of_landmarks)
    # Instantiate helicopter
    helicopter = Helicopter(heliport, sd_distance, sd_angle)
    # Instantiate particle filter
    particle_filter = ParticleFilter(number_of_particles, [heliport.size_x, heliport.size_y], sd_distance, sd_angle)
    # Instantiate presentation layer
    presentation = Presentation(heliport)

    # Start simulation
    number_of_steps = helicopter.z

    # Variable for adding up the actual distance traveled by the helicopter
    actual_distance = 0

    # Print start coordinates
    if print_results:
        print(f"Start coordinates: x = {helicopter.x}, y = {helicopter.y}, z = {helicopter.z}, theta = {helicopter.theta} \n")

    # 1. Initialize particles
    particles = particle_filter.initialize_particles()

    # 2. Move helicopter for the first time
    desired_distance = helicopter.measure_00(helicopter.x, helicopter.y)[0] / number_of_steps
    desired_rotation = helicopter.measure_00(helicopter.x, helicopter.y)[1] - helicopter.theta
    helicopter.move(desired_distance, desired_rotation)
    actual_distance += desired_distance

    # Repeat for each step
    while number_of_steps > 0:

        # 3. Particle filter algorithm
        # 3.1. Update particles
        particles = particle_filter.update_particles(particles, desired_distance, desired_rotation)

        # 3.2. Update weights based on measurements
        measurements = helicopter.measure_lm(heliport)
        particles = particle_filter.compute_likelihood(particles, measurements, heliport.landmarks)

        # 3.3. Normalize weights
        particles = particle_filter.normalize_weights(particles)

        # Plot a PDF (if chosen)
        if plot_type == "PDF":
            presentation.plot_pdf(particles, pdf_variable)

        # 3.4. Resample particles
        if resampling_method == "systematic":
            particles = particle_filter.systematic_resample(particles)
        else:
            particles = particle_filter.multinomial_resampling(particles)

        # 4. Get state estimates
        estimated_state = particle_filter.estimate_state(particles)

        # 5. Move helicopter to the new state
        desired_distance = helicopter.measure_00(estimated_state[0], estimated_state[1])[0] / number_of_steps
        desired_rotation = helicopter.measure_00(helicopter.x, helicopter.y)[1] - helicopter.theta
        helicopter.move(desired_distance, desired_rotation)
        actual_distance += desired_distance

        # Visualize current position (if chosen)
        if plot_type == "observations":
            presentation.visualise(particles, helicopter)

        # Lower value of number of steps
        helicopter.z -= 1
        number_of_steps -= 1
    
    # Print end coordinates
    if print_results:
        print(f"End coordinates: x = {helicopter.x}, y = {helicopter.y}, z = {helicopter.z}, theta = {helicopter.theta} \n")

    # Calculate diff between ideal path and actual distance
    actual_distance += helicopter.get_00_dt([helicopter.x, helicopter.y]) # Add missing distance to point (0, 0)
    ideal_distance = helicopter.get_00_dt(helicopter.starting_point)

    return helicopter.get_actual_position(), helicopter.actual, particle_filter.predicted, actual_distance, ideal_distance