import random

def generate_complex_domain_pddl(domain_file):
    with open(domain_file, "w") as file:
        file.write("""(define (domain complex_navigation)
    (:requirements :strips :typing :equality :conditional-effects)
    (:types 
        location
        dead_end
        key - location
    )
    (:predicates
        (path ?from - location ?to - location)
        (dead_end_path ?from - location ?to - dead_end)
        (visited ?loc - location)
        (key_at ?loc - key)
        (has_key)
        (at ?loc - location)
    )
    (:action move
        :parameters (?from ?to - location)
        :precondition (and (at ?from) (path ?from ?to) (not (visited ?to)))
        :effect (and (not (at ?from)) (at ?to) (visited ?to))
    )
    (:action move_to_dead_end
        :parameters (?from - location ?to - dead_end)
        :precondition (and (at ?from) (dead_end_path ?from ?to))
        :effect (and (not (at ?from)))
    )
    (:action pick_up_key
        :parameters (?loc - key)
        :precondition (and (at ?loc) (key_at ?loc) (not (has_key)))
        :effect (and (not (key_at ?loc)) (has_key))
    )
)""")
    print(f"Domain file generated: {domain_file}")

def generate_complex_problem_pddl(num_locations, num_dead_ends, problem_file):
    locations = [f"loc{i}" for i in range(1, num_locations + 1)]
    dead_ends = [f"dead{i}" for i in range(1, num_dead_ends + 1)]
    keys = [f"key{i}" for i in range(1, 5)]  # Few key locations

    with open(problem_file, "w") as file:
        file.write("(define (problem extended_navigation_problem)\n")
        file.write("  (:domain complex_navigation)\n")
        file.write("  (:objects\n    ")
        file.write(" ".join(locations) + " - location\n    ")
        file.write(" ".join(dead_ends) + " - dead_end\n    ")
        file.write(" ".join(keys) + " - key\n  )\n")
        file.write("  (:init\n    (at loc1)\n")

        # Paths between locations
        for loc in locations:
            connections = random.sample(locations, random.randint(4, 10))
            for conn in connections:
                if conn != loc:
                    file.write(f"    (path {loc} {conn})\n")

        # Paths to dead ends
        for loc in locations:
            dead_end_conn = random.choice(dead_ends)
            file.write(f"    (dead_end_path {loc} {dead_end_conn})\n")

        # Key locations
        for key in keys:
            key_location = random.choice(locations)
            file.write(f"    (key_at {key} {key_location})\n")

        file.write("  )\n")
        file.write("  (:goal (and (visited loc150) (has_key)) )\n")  # Example goal
        file.write(")\n")

    print(f"Problem file generated: {problem_file}")

# Generate domain and problem files
generate_complex_domain_pddl("domain.pddl")
generate_complex_problem_pddl(300, 300, "pfile1")  # Increase numbers as needed
