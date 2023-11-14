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
# Function to generate a new PDDL problem file
def generate_problem_file(car_location, truck_location, car_battery, truck_behavior, traffic_conditions):
    with open("autonomous_car_problem.pddl", "w") as file:
        file.write(f"""
(define (problem car_route)
  (:domain autonomous_car)

  (:objects 
    car1 - car
    {' '.join(LOCATIONS)} - location
    high medium low - fuel_level
    safe close very_close cut_into - truck_state
  )

  (:init 
    (car_at car1 {car_location})
    (truck_at {truck_location})
    (fuel_level car1 high)
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
            f"Problem file for location {car_location}, truck at {truck_location}, battery at {car_battery}, truck behavior {truck_behavior} generated.")


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
        "--dispatch-threshold", "0.025",
        domain_file, problem_file
    ]

    if solver_type == 'disp':
        base_command.insert(-2, "--use-dispatcher")
        base_command.insert(-2, "LPFThreshold")

    result = subprocess.run(base_command, capture_output=True, text=True)
    return result.stdout

# Simulation logic
def simulate(domain_file):
    car_location = random.choice(LOCATIONS)
    truck_location = random.choice(LOCATIONS)
    car_battery = CAR_INITIAL_BATTERY
    truck_behavior = random.choice(TRUCK_BEHAVIORS)
    traffic_conditions = [random.choice(TRAFFIC_LEVELS) for _ in LOCATIONS]

    generate_problem_file(car_location, truck_location, car_battery, truck_behavior, traffic_conditions)
    no_disp_plan = call_solver('no-disp', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')
    disp_plan = call_solver('disp', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')

    return car_location, truck_location, car_battery, truck_behavior, no_disp_plan, disp_plan


# Update UI with simulation results
def update_ui(root, result_text_widget, domain_file):
    car_location, truck_location, car_battery, truck_behavior, no_disp_plan, disp_plan = simulate(domain_file)
    result_text_widget.delete('1.0', tk.END)  # Clear the existing text
    result_text_widget.insert(tk.END, f"Car at: {car_location}\n")
    result_text_widget.insert(tk.END, f"Truck at: {truck_location}\n")
    result_text_widget.insert(tk.END, f"Battery Level: {car_battery}\n")
    result_text_widget.insert(tk.END, f"Truck Behavior: {truck_behavior}\n")
    result_text_widget.insert(tk.END, f"No Disp Plan:\n{no_disp_plan}\n")
    result_text_widget.insert(tk.END, f"Disp Plan:\n{disp_plan}\n")

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
