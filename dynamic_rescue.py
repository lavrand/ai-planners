import random

def generate_pddl_domain():
    domain_str = """
(define (domain dynamic_rescue)
    (:requirements :strips :typing)
    (:types location - object)
    (:predicates
        (robot_at ?loc - location)
        (target_at ?loc - location)
        (obstacle_at ?loc - location)
        (rescued ?loc - location)
    )
    (:action move
        :parameters (?from ?to - location)
        :precondition (and (robot_at ?from) (not (obstacle_at ?to)))
        :effect (and (not (robot_at ?from)) (robot_at ?to))
    )
    (:action scan_for_target
        :parameters (?loc - location)
        :precondition (robot_at ?loc)
        :effect (when (target_at ?loc) (rescued ?loc))
    )
)
"""
    with open("dynamic_rescue_domain.pddl", "w") as domain_file:
        domain_file.write(domain_str)

def generate_pddl_problem(num_locations, targets, time_limit=0.5):
    # Introducing dynamic obstacles and changing targets
    dynamic_obstacles = [random.randint(0, num_locations - 1) for _ in range(num_locations // 2)]
    dynamic_targets = [random.choice(targets) for _ in range(len(targets))]

    problem_str = f"""
(define (problem dynamic_rescue_problem)
    (:domain dynamic_rescue)
    (:objects
        {" ".join(f"loc{i}" for i in range(num_locations))} - location
    )
    (:init
        (robot_at loc0)
        {" ".join(f"(target_at loc{target})" for target in dynamic_targets)}
        {" ".join(f"(obstacle_at loc{obs})" for obs in dynamic_obstacles)}
    )
    (:goal (and {" ".join(f"(rescued loc{target})" for target in targets)})
    )
)
"""
    with open("pfile1", "w") as problem_file:
        problem_file.write(problem_str)

generate_pddl_domain()
generate_pddl_problem(10, [2, 5, 7])