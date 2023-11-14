import random

def generate_pddl_domain_advanced():
    # Domain with more complex actions and interdependencies
    domain_str = """
(define (domain complex_rescue)
    (:requirements :strips :typing :durative-actions :fluents)
    (:types location - object)
    (:predicates
        (robot_at ?loc - location)
        (target_at ?loc - location)
        (obstacle_at ?loc - location)
        (rescued ?loc - location)
        (available ?act - action)
    )
    (:durative-action move
        :parameters (?from ?to - location)
        :duration (= ?duration 1)
        :condition (and (over all (robot_at ?from)) (over all (not (obstacle_at ?to))))
        :effect (and (at end (not (robot_at ?from))) (at end (robot_at ?to)))
    )
    (:durative-action rescue
        :parameters (?loc - location)
        :duration (= ?duration 2)
        :condition (and (over all (robot_at ?loc)) (at start (target_at ?loc)))
        :effect (at end (rescued ?loc))
    )
    (:action change_goal
        :parameters (?new_target - location)
        :precondition (available change_goal)
        :effect (and (not (available change_goal)) (target_at ?new_target))
    )
    ; Additional complex actions can be added here
)
"""
    with open("complex_rescue_domain.pddl", "w") as domain_file:
        domain_file.write(domain_str)

def generate_pddl_problem_advanced(num_locations, targets):
    # Dynamic targets and obstacles
    dynamic_obstacles = [random.randint(0, num_locations - 1) for _ in range(num_locations // 2)]
    dynamic_targets = [random.choice(targets) for _ in range(len(targets))]

    problem_str = f"""
(define (problem complex_rescue_problem)
    (:domain complex_rescue)
    (:objects
        {" ".join(f"loc{i}" for i in range(num_locations))} - location
    )
    (:init
        (robot_at loc0)
        {" ".join(f"(target_at loc{target})" for target in dynamic_targets)}
        {" ".join(f"(obstacle_at loc{obs})" for obs in dynamic_obstacles)}
        (available change_goal)
    )
    (:goal (and {" ".join(f"(rescued loc{target})" for target in targets)})
    )
)
"""
    with open("pfile1", "w") as problem_file:
        problem_file.write(problem_str)

generate_pddl_domain_advanced()
generate_pddl_problem_advanced(20, [2, 5, 7, 10, 12, 15])
