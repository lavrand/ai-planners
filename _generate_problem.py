import random

def generate_pddl_problem(num_locations, output_file):
    locations = [f"loc{i}" for i in range(1, num_locations + 1)]

    with open(output_file, "w") as file:
        file.write("(define (problem extended_navigation_problem)\n")
        file.write("  (:domain complex_navigation)\n")
        file.write("  (:objects\n    ")
        file.write(" ".join(locations))
        file.write(" - location\n  )\n")
        file.write("  (:init\n    (at loc1)\n")

        # Generating a complex web of paths
        for i in range(1, num_locations):
            # Create paths from each location to a few random other locations
            connections = random.sample(locations, random.randint(2, 4))
            for conn in connections:
                if conn != f"loc{i}":
                    file.write(f"    (path loc{i} {conn})\n")

        file.write("  )\n")
        file.write(f"  (:goal\n    (at loc{num_locations})\n  )\n")
        file.write(")\n")

    print(f"Problem file generated: {output_file}")

# Change the number of locations as needed
generate_pddl_problem(50, "pfile1")
