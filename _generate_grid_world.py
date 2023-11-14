# Convert the current state to PDDL problem file
# Define the grid size
GRID_SIZE = 5

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