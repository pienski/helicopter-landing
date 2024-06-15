from run_simulation import run_simulation
import numpy as np

# Testing variables
number_of_particles = 1500
number_of_landmarks = 3
sd_distance = 0.25
sd_angle = 0.05
plot_type = "N/A"
pdf_variable = "N/A"
resampling_method = "multinomial" # possible values = ("systematic", "multinomial")

success_criteria = 0.5 # Size of a box that counts as a successful landing
test_count = 100 # Number of test iterations

# Calculating RMSE
def calculate_rmse(actual, predicted):
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    return rmse

actual = []
predicted = []

success_count = 0
rmse = 0

actual_distance_total = 0
ideal_distance_total = 0

for i in range(test_count):
    simulation_results, actual_run, predicted_run, actual_distance, ideal_distance = run_simulation(number_of_particles, number_of_landmarks, sd_distance, sd_angle, plot_type, pdf_variable, resampling_method, False)
    
    # Conditions for success calculations
    if abs(simulation_results[0]) < success_criteria and abs(simulation_results[1]) < success_criteria:
        success_count += 1
        print(f"Test #{i+1}: success. {simulation_results}")
    else:
        print(f"Test #{i+1}: failure. {simulation_results}")

    # Append actual and predicted results
    actual.append(actual_run[1:])
    predicted.append(predicted_run)

    # Add distance
    actual_distance_total += actual_distance
    ideal_distance_total += ideal_distance

# Success rate results
success_rate = success_count / test_count
print(f"Success rate: {success_rate}")

# RMSE results
actual = np.array(actual[0])
predicted = np.array(predicted[0])

actual_x = actual[:, 0]
actual_y = actual[:, 1]
actual_theta = actual[:, 2]
predicted_x = predicted[:, 0]
predicted_y = predicted[:, 1]
predicted_theta = predicted[:, 2]

rmse_x = calculate_rmse(actual_x, predicted_x)
rmse_y = calculate_rmse(actual_y, predicted_y)
rmse_theta = calculate_rmse(actual_theta, predicted_theta)
print(f"RMSE for x: {rmse_x}")
print(f"RMSE for y: {rmse_y}")
print(f"RMSE for theta: {rmse_theta}")

# Surplus distance calc
surplus_distance_pct = round((actual_distance_total - ideal_distance_total) / ideal_distance_total, 4)
print(f"Surplus distance pct: {surplus_distance_pct}")