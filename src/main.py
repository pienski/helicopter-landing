from run_simulation import run_simulation

def get_valid_input(prompt):
    while True:
        response = input(prompt).lower()
        if response == 'yes' or response == 'no':
            return response
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


is_default = get_valid_input("Do you want to use default parameters? (yes/no):")

if is_default == "yes":
    # default variables
    number_of_particles = 3000
    number_of_landmarks = 3
    sd_distance = 0.25
    sd_angle = 0.05
    plot_type = "observations" # possible values = ("observations", "PDF")
    pdf_variable = "theta" # possible values = ("x", "y", "theta")
    resampling_method = "systematic" # possible values = ("systematic", "multinomial")
else:
    number_of_particles = int(input("Number of particles (int):"))
    number_of_landmarks = int(input("Number of landmarks (int):"))
    sd_distance = float(input("Standard deviation of distance (float):"))
    sd_angle = float(input("Standard deviation of angle (float):"))
    plot_type = input("Plot type (observations/PDF):")
    if plot_type == "PDF":
        pdf_variable = input("State variable on the PDF plot (x/y/theta):")
    else:
        pdf_variable = "x"
    resampling_method = input("Resampling method (systematic/multinomial):")

run_simulation(number_of_particles, number_of_landmarks, sd_distance, sd_angle, plot_type, pdf_variable, resampling_method)