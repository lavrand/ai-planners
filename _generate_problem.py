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

        # Creating paths
        all_possible_paths = set((f"loc{i}", f"loc{j}") for i in range(1, num_locations) for j in range(1, num_locations) if i != j)
        chosen_paths = set(random.sample(all_possible_paths, num_locations * 3))  # Increase the number of paths

        for from_loc, to_loc in chosen_paths:
            file.write(f"    (path {from_loc} {to_loc})\n")

        file.write("  )\n")
        file.write(f"  (:goal\n    (at loc{num_locations})\n  )\n")
        file.write(")\n")

    print(f"Problem file generated: {output_file}")

# Increase the number of locations to increase complexity
generate_pddl_problem(100, "pfile")  # Example with 100 locations
