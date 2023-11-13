import random

def generate_complex_pddl_problem(num_locations, output_file):
    locations = [f"loc{i}" for i in range(1, num_locations + 1)]

    with open(output_file, "w") as file:
        file.write("(define (problem extended_navigation_problem)\n")
        file.write("  (:domain complex_navigation)\n")
        file.write("  (:objects\n    ")
        file.write(" ".join(locations))
        file.write(" - location\n  )\n")
        file.write("  (:init\n    (at loc1)\n")

        # Creating a dense and complex network of paths
        for loc in locations:
            connections = random.sample(locations, random.randint(5, 10))  # Increase connections per location
            for conn in connections:
                if conn != loc:
                    file.write(f"    (path {loc} {conn})\n")

        # Introducing dead ends
        for _ in range(num_locations // 2):
            dead_end_from = random.choice(locations)
            dead_end_to = f"dead{random.randint(1, num_locations)}"
            file.write(f"    (path {dead_end_from} {dead_end_to})\n")

        file.write("  )\n")
        file.write(f"  (:goal\n    (at loc{num_locations})\n  )\n")
        file.write(")\n")

    print(f"Problem file generated: {output_file}")

generate_complex_pddl_problem(150, "pfile1")  # Example with 150 locations
