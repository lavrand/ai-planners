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

        # Creating a guaranteed solvable main path
        for i in range(1, num_locations):
            file.write(f"    (path loc{i} loc{i+1})\n")

        # Adding extra paths for complexity
        all_possible_paths = set((f"loc{i}", f"loc{j}") for i in range(1, num_locations) for j in range(1, num_locations) if i != j)
        main_path = set((f"loc{i}", f"loc{i+1}") for i in range(1, num_locations))
        extra_paths = all_possible_paths - main_path

        for _ in range(num_locations * 2):  # Limit the number of extra paths
            from_loc, to_loc = random.sample(extra_paths, 1)[0]
            file.write(f"    (path {from_loc} {to_loc})\n")
            extra_paths.remove((from_loc, to_loc))

        file.write("  )\n")
        file.write(f"  (:goal\n    (at loc{num_locations})\n  )\n")
        file.write(")\n")

    print(f"Problem file generated: {output_file}")

generate_pddl_problem(50, "pfile1")