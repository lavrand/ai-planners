import os
import random
import subprocess
import tkinter as tk

# Constants for simulation
LOCATIONS = ['loc1', 'loc2', 'loc3', 'loc4']
TRUCK_BEHAVIORS = ['safe', 'close', 'very_close']

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
    # Example command, adjust based on your solver's requirements
    result = subprocess.run([solver_type, domain_file, problem_file], capture_output=True)
    return result.stdout

# Simulation logic
def simulate():
    car_location = random.choice(LOCATIONS)
    truck_location = random.choice(LOCATIONS)
    fuel_level = 'high'
    truck_behavior = random.choice(TRUCK_BEHAVIORS)

    generate_problem_file(car_location, truck_location, fuel_level, truck_behavior)
    offline_plan = call_solver('offline_solver', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')
    online_plan = call_solver('online_solver', 'autonomous_car_domain.pddl', 'autonomous_car_problem.pddl')

    return car_location, truck_location, fuel_level, truck_behavior, offline_plan, online_plan

# Update UI with simulation results
def update_ui(root, result_label):
    car_location, truck_location, fuel_level, truck_behavior, offline_plan, online_plan = simulate()
    result_label.config(text=f"Car at: {car_location}\nTruck at: {truck_location}\nFuel: {fuel_level}\nTruck Behavior: {truck_behavior}\nOffline Plan: {offline_plan}\nOnline Plan: {online_plan}")

# UI setup
root = tk.Tk()
root.title("Autonomous Car Simulation")
result_label = tk.Label(root, text="Simulation Results", justify=tk.LEFT)
result_label.pack()
update_button = tk.Button(root, text="Run Simulation", command=lambda: update_ui(root, result_label))
update_button.pack()
root.mainloop()
