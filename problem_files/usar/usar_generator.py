import random


def create_usar_domain():
    domain_content = """
    (define (domain usar)
      (:requirements :strips :typing :durative-actions :fluents :timed-initial-literals)
      (:types robot victim debris area)
      (:functions
        (battery-level ?r - robot)
        (distance ?from ?to - area)
      )
      (:predicates
        (robot-at ?r - robot ?a - area)
        (victim-at ?v - victim ?a - area)
        (debris-at ?d - debris ?a - area)
        (victim-rescued ?v - victim)
        (debris-cleared ?d - debris)
        (robot-functional ?r - robot)
      )
      
      (:durative-action move
        :parameters (?r - robot ?from ?to - area)
        :duration (= ?duration (distance ?from ?to))
        :condition (and (at start (robot-at ?r ?from)) (over all (robot-functional ?r)))
        :effect (and (at start (not (robot-at ?r ?from))) (at end (robot-at ?r ?to)))
      )
    
      (:durative-action perform-task
        :parameters (?r - robot ?t - task ?a - area)
        :duration (= ?duration (task-duration ?t))
        :condition (and (at start (robot-at ?r ?a)) (at start (task-at ?t ?a)) (over all (robot-functional ?r)))
        :effect (at end (task-completed ?t))
      )
    
      (:durative-action clear-debris
        :parameters (?r - robot ?d - debris ?a - area)
        :duration (= ?duration 10)
        :condition (and (at start (robot-at ?r ?a)) (over all (debris-at ?d ?a)) (over all (robot-functional ?r)))
        :effect (at end (not (debris-at ?d ?a)))
      )
    )
    """
    return domain_content


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


# Example usage
domain_content = create_usar_domain()
problem_content = create_usar_problem()

# Output the domain and problem content
print(domain_content)
print(problem_content)
