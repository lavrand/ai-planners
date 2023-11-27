import random
import os


def create_usar_problem(num_robots=3, num_victims=5, num_debris=5, num_areas=10):
    robots = ' '.join([f'robot{i + 1}' for i in range(num_robots)]) + " - robot"
    victims = ' '.join([f'victim{i + 1}' for i in range(num_victims)]) + " - victim"
    debris = ' '.join([f'debris{i + 1}' for i in range(num_debris)]) + " - debris"
    areas = ' '.join([f'area{i + 1}' for i in range(num_areas)]) + " - area"

    robot_locations = '\n        '.join(
        [f'(robot-at robot{i + 1} area{random.randint(1, num_areas)})' for i in range(num_robots)])
    victim_locations = '\n        '.join(
        [f'(victim-at victim{i + 1} area{random.randint(1, num_areas)})' for i in range(num_victims)])
    debris_locations = '\n        '.join(
        [f'(debris-at debris{i + 1} area{random.randint(1, num_areas)})' for i in range(num_debris)])
    battery_levels = '\n        '.join(
        [f'(= (battery-level robot{i + 1}) {random.uniform(50.0, 100.0):.2f})' for i in range(num_robots)])
    distances = '\n        '.join(
        [f'(= (distance area{i + 1} area{j + 1}) {random.uniform(1.0, 10.0):.6f})' for i in range(num_areas) for j in
         range(num_areas) if i != j])
    timed_goals = '\n        '.join(
        [f'(at {random.randint(100, 1000)} (victim-rescued victim{i + 1}))' for i in range(num_victims)])
    rescue_goals = '\n        '.join([f'(victim-rescued victim{i + 1})' for i in range(num_victims)])
    clearance_goals = '\n        '.join([f'(debris-cleared debris{i + 1})' for i in range(num_debris)])

    problem_content = f"""
    (define (problem usar-instance)
      (:domain usar)
      (:objects
        {robots}
        {victims}
        {debris}
        {areas}
      )
      (:init
        {robot_locations}
        {victim_locations}
        {debris_locations}
        {battery_levels}
        {distances}
        {timed_goals}
      )
      (:goal (and
        {rescue_goals}
        {clearance_goals}
      ))
    )
    """
    return problem_content


# Creating 500 problem files
for i in range(2, 501):
    problem_filename = f'pfile{i}'
    problem_content = create_usar_problem()
    with open(problem_filename, 'w') as file:
        file.write(problem_content)
    print(f"Created file: {problem_filename}")
