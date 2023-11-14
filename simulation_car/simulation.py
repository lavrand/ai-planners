import os
import random
import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Constants for simulation
LOCATIONS = ['loc1', 'loc2', 'loc3', 'loc4']
TRUCK_BEHAVIORS = ['safe', 'close', 'very_close', 'cut_into']

# Function to generate a new PDDL problem file
def generate_problem_file(car_location, truck_location, fuel_level, truck_behavior):
    with open("autonomous_car_problem.pddl", "w") as file:
        file.write(f"""
(define (problem car_route)
  (:domain autonomous_car)
  (:objects 
    car1 - car 
    { ' '.join(LOCATIONS) } - location
  )

  (:init 
    (car_at car1 {car_location}) 
    (truck_at {truck_location})
    (fuel_level car1 {fuel_level}) 
    (distance_to_truck car1 {truck_behavior})
    {" ".join(f"(road_between {loc1} {loc2})" for loc1 in LOCATIONS for loc2 in LOCATIONS if loc1 != loc2)}
  )

  (:goal 
    (and (car_at car1 loc4) (distance_to_truck car1 safe))
  )
)
""")

# Function to call the PDDL solver
def call_solver(solver_type, domain_file, problem_file):
    base_command = "../rewrite-no-lp --time-based-on-expansions-per-second 500 " \
                   "--include-metareasoning-time --multiply-TILs-by 1 " \
                   "--real-to-plan-time-multiplier 1 --calculate-Q-interval 100 " \
                   "--add-weighted-f-value-to-Q -0.000001 --min-probability-failure 0.001 " \
                   "--slack-from-heuristic --forbid-self-overlapping-actions " \
                   "--deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 " \
                   "--icaps-for-n-expansions 100 --time-aware-heuristic 1 " \
                   "--dispatch-frontier-size 10 --subtree-focus-threshold 0.025 " \
                   "--dispatch-threshold 0.025 "

    if solver_type == 'disp':
        command = base_command + "--use-dispatcher LPFThreshold "
    else:  # 'no-disp'
        command = base_command

    command += f"{domain_file} {problem_file}"
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout

# Simulation logic
def simulate():
    car_location = random.choice(LOCATIONS)
    truck_location = random.choice(LOCATIONS)
    fuel_level = 'high'
    truck_behavior = random.choice(TRUCK_BEHAVIORS)

    # Simulate the 'cut-into' event when truck behavior is 'very_close'
    if truck_behavior == 'very_close':
        truck_behavior = 'cut_into'

    generate_problem_file(car_location, truck_location, fuel_level, truck_behavior)
    no_disp_plan = call_solver('no-disp', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')
    disp_plan = call_solver('disp', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')

    return car_location, truck_location, fuel_level, truck_behavior, no_disp_plan.decode(), disp_plan.decode()


# Update UI with simulation results
def update_ui(root, result_text_widget):
    car_location, truck_location, fuel_level, truck_behavior, no_disp_plan, disp_plan = simulate()
    result_text_widget.delete('1.0', tk.END)  # Clear the existing text
    result_text_widget.insert(tk.END, f"Car at: {car_location}\n")
    result_text_widget.insert(tk.END, f"Truck at: {truck_location}\n")
    result_text_widget.insert(tk.END, f"Fuel: {fuel_level}\n")
    result_text_widget.insert(tk.END, f"Truck Behavior: {truck_behavior}\n")
    result_text_widget.insert(tk.END, f"No-Disp Plan: {no_disp_plan}\n")
    result_text_widget.insert(tk.END, f"Disp Plan: {disp_plan}\n")

# UI setup
root = tk.Tk()
root.title("Autonomous Car Simulation")

# Using ScrolledText widget which includes a scrollbar
result_text_widget = ScrolledText(root, height=15, width=100)
result_text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

update_button = tk.Button(root, text="Run Simulation", command=lambda: update_ui(root, result_text_widget))
update_button.pack(side=tk.BOTTOM)

root.mainloop()