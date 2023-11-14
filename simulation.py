import os
import subprocess
import random
import time

# Define the grid size
GRID_SIZE = 5

# Define initial robot position
robot_position = [0, 0]

# Define the goal position
goal_position = [GRID_SIZE - 1, GRID_SIZE - 1]

# Generate a random obstacle
def generate_obstacle():
    return [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Convert the current state to PDDL problem file
def create_pddl_problem(robot_pos, goal_pos, obstacle_pos):
    problem_str = f"""
(define (problem grid_world)
    (:domain grid_navigation)
    (:objects {" ".join([f"cell{x}{y}" for x in range(GRID_SIZE) for y in range(GRID_SIZE)])} - cell)
    (:init
        (robot_at cell{robot_pos[0]}{robot_pos[1]})
        (goal_at cell{goal_pos[0]}{goal_pos[1]})
        {"(obstacle_at cell{}{})".format(*obstacle_pos) if obstacle_pos else ""}
        {" ".join([f"(adjacent cell{x}{y} cell{x}{(y+1)})" for x in range(GRID_SIZE) for y in range(GRID_SIZE - 1)])}
        {" ".join([f"(adjacent cell{x}{y} cell{(x+1)}{y})" for x in range(GRID_SIZE - 1) for y in range(GRID_SIZE)])}
    )
    (:goal (robot_at cell{goal_pos[0]}{goal_pos[1]}))
)
"""
    with open("grid_world_problem.pddl", "w") as file:
        file.write(problem_str)

# Call the PDDL planner
def call_planner(domain_file, problem_file):
    result = subprocess.run(['fast-downward-23.06', domain_file, problem_file], capture_output=True, text=True)
    return result.stdout

# Main simulation loop
def simulation_loop():
    while robot_position != goal_position:
        obstacle_position = generate_obstacle() if random.random() < 0.3 else None  # 30% chance of an obstacle appearing

        create_pddl_problem(robot_position, goal_position, obstacle_position)

        plan = call_planner("grid_navigation_domain.pddl", "grid_world_problem.pddl")
        # Process the plan to update robot_position
        # ...

        time.sleep(0.5)  # Adjust the time delay as needed for your simulation

# Define your PDDL domain here or load it from a file
grid_navigation_domain = """
(define (domain grid_navigation)
    (:requirements :strips)
    (:predicates
        (robot_at ?cell - cell)
        (goal_at ?cell - cell)
        (obstacle_at ?cell - cell)
        (adjacent ?cell1 ?cell2 - cell)
    )

    (:action move
        :parameters (?from ?to - cell)
        :precondition (and (robot_at ?from) 
                           (adjacent ?from ?to) 
                           (not (obstacle_at ?to)))
        :effect (and (not (robot_at ?from)) 
                     (robot_at ?to))
    )
)

"""

# Write the domain file
with open("grid_navigation_domain.pddl", "w") as file:
    file.write(grid_navigation_domain)

simulation_loop()
