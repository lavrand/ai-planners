import os
import random
import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Constants for simulation
LOCATIONS = ['loc1', 'loc2', 'loc3', 'loc4']
TRAFFIC_LEVELS = ['low', 'medium', 'high']
TRUCK_BEHAVIORS = ['safe', 'close', 'very_close', 'cut_into']
CAR_INITIAL_BATTERY = 100

# Function to generate a new PDDL problem file
def generate_problem_file(car_location, truck_location, car_battery, truck_behavior, traffic_conditions):
    with open("autonomous_car_problem.pddl", "w") as file:
        file.write(f"""
(define (problem car_route)
  (:domain autonomous_car)

  (:objects 
    car1 - car
    {' '.join(LOCATIONS)} - location
  )

  (:init 
    (car_at car1 {car_location})
    (truck_at {truck_location})
    (fuel_status car1 high)  ; Updated to use fuel_status
    {" ".join(f"(road_between {loc1} {loc2})" for loc1 in LOCATIONS for loc2 in LOCATIONS if loc1 != loc2)}
    {" ".join(f"(traffic {loc} {traffic_conditions[i]})" for i, loc in enumerate(LOCATIONS))}
    (truck_behavior {truck_behavior})
    (= (battery_level car1) {car_battery})
  )

  (:goal 
    (and (car_at car1 loc4)
         (not (truck_behavior cut_into)))
  )
)
""")
        print(
            f"Problem file generated for location {car_location}, truck at {truck_location}, battery at {car_battery}, truck behavior {truck_behavior}.")

# Function to call the PDDL solver
def call_solver(solver_type, domain_file, problem_file):
    base_command = [
        "../rewrite-no-lp",
        "--time-based-on-expansions-per-second", "500",
        "--include-metareasoning-time",
        "--multiply-TILs-by", "1",
        "--real-to-plan-time-multiplier", "1",
        "--calculate-Q-interval", "100",
        "--add-weighted-f-value-to-Q", "-0.000001",
        "--min-probability-failure", "0.001",
        "--slack-from-heuristic",
        "--forbid-self-overlapping-actions",
        "--deadline-aware-open-list", "IJCAI",
        "--ijcai-gamma", "1",
        "--ijcai-t_u", "100",
        "--icaps-for-n-expansions", "100",
        "--time-aware-heuristic", "1",
        "--dispatch-frontier-size", "10",
        "--subtree-focus-threshold", "0.025",
        "--dispatch-threshold", "0.025"
    ]

    if solver_type == 'disp':
        base_command += ["--use-dispatcher", "LPFThreshold"]

    # Append the domain and problem files without flags
    base_command += [domain_file, problem_file]

    result = subprocess.run(base_command, capture_output=True, text=True)
    return result.stdout, result.stderr



# Simulation logic
def simulate(domain_file):
    car_location = random.choice(LOCATIONS)
    truck_location = random.choice(LOCATIONS)
    car_battery = CAR_INITIAL_BATTERY
    truck_behavior = random.choice(TRUCK_BEHAVIORS)
    traffic_conditions = [random.choice(TRAFFIC_LEVELS) for _ in LOCATIONS]

    # Decode the solver output
    def decode_solver_output(output):
        # Split the output by new lines and filter out empty lines
        lines = [line.strip() for line in output.split('\n') if line.strip()]

        # Extract plan details
        plan_details = [line for line in lines if line.startswith(';') or line.startswith('0.001:')]

        # Extract warnings
        warnings = [line for line in lines if line.startswith('Warning:')]

        # Join the extracted details into multi-line strings for better readability
        plan_str = '\n'.join(plan_details)
        warnings_str = '\n'.join(warnings)

        return plan_str, warnings_str

    # Call the solver and decode its output
    no_disp_output, no_disp_errors = call_solver('no-disp', domain_file, 'autonomous_car_problem.pddl')
    no_disp_plan, no_disp_warnings = decode_solver_output(no_disp_output)

    disp_output, disp_errors = call_solver('disp', domain_file, 'autonomous_car_problem.pddl')
    disp_plan, disp_warnings = decode_solver_output(disp_output)

    return car_location, truck_location, car_battery, truck_behavior, no_disp_plan, no_disp_warnings, disp_plan, disp_warnings

# Update UI with simulation results
def update_ui(root, result_text_widget, domain_file):
    car_location, truck_location, car_battery, truck_behavior, no_disp_plan, no_disp_warnings, disp_plan, disp_warnings = simulate(domain_file)
    result_text_widget.delete('1.0', tk.END)  # Clear the existing text
    result_text_widget.insert(tk.END, f"Car at: {car_location}\n")
    result_text_widget.insert(tk.END, f"Truck at: {truck_location}\n")
    result_text_widget.insert(tk.END, f"Battery Level: {car_battery}\n")
    result_text_widget.insert(tk.END, f"Truck Behavior: {truck_behavior}\n")
    result_text_widget.insert(tk.END, f"No Disp Plan:\n{no_disp_plan}\n")
    result_text_widget.insert(tk.END, f"No Disp Warnings:\n{no_disp_warnings}\n")
    result_text_widget.insert(tk.END, f"Disp Plan:\n{disp_plan}\n")
    result_text_widget.insert(tk.END, f"Disp Warnings:\n{disp_warnings}\n")

# UI setup
root = tk.Tk()
root.title("Autonomous Car Simulation")

# Using ScrolledText widget which includes a scrollbar
result_text_widget = ScrolledText(root, height=20, width=80)
result_text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

domain_file = "autonomous_car_domain.pddl"  # Adjust if your domain file is named differently

update_button = tk.Button(root, text="Run Simulation",
                          command=lambda: update_ui(root, result_text_widget, domain_file))
update_button.pack(side=tk.BOTTOM)

root.mainloop()
