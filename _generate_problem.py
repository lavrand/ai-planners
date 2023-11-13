import random

def generate_domain_pddl(domain_file):
    with open(domain_file, "w") as file:
        file.write("""(define (domain complex_navigation)
    (:requirements :strips :typing :equality)
    (:types 
        location
        dead_end
    )
    (:predicates
        (path ?from - location ?to - location)
        (dead_end_path ?from - location ?to - dead_end)
        (visited ?loc - location)
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
)""")
    print(f"Domain file generated: {domain_file}")

def generate_problem_pddl(num_locations, num_dead_ends, problem_file):
    locations = [f"loc{i}" for i in range(1, num_locations + 1)]
    dead_ends = [f"dead{i}" for i in range(1, num_dead_ends + 1)]
    key_locations = random.sample(locations, 5)  # Select key locations for complex goals

    with open(problem_file, "w") as file:
        file.write("(define (problem extended_navigation_problem)\n")
        file.write("  (:domain complex_navigation)\n")
        file.write("  (:objects\n    ")
        file.write(" ".join(locations) + " - location\n    ")
        file.write(" ".join(dead_ends) + " - dead_end\n  )\n")
        file.write("  (:init\n    (at loc1)\n")

        # Paths between locations
        for loc in locations:
            connections = random.sample(locations, random.randint(4, 8))
            for conn in connections:
                if conn != loc:
                    file.write(f"    (path {loc} {conn})\n")

        # Paths to dead ends
        for loc in locations:
            dead_end_conn = random.choice(dead_ends)
            file.write(f"    (dead_end_path {loc} {dead_end_conn})\n")

        file.write("  )\n")
        file.write("  (:goal (and ")
        for loc in key_locations:
            file.write(f"(visited {loc}) ")
        file.write("))\n")
        file.write(")\n")

    print(f"Problem file generated: {problem_file}")

# Generate domain and problem files
generate_domain_pddl("domain.pddl")
generate_problem_pddl(200, 200, "pfile1")  # Adjust numbers as needed
