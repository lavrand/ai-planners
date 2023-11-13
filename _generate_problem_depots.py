import random

def generate_depot_domain_pddl(domain_file):
    with open(domain_file, "w") as file:
        file.write("""(define (domain Depot)
    (:requirements :typing :durative-actions :fluents)
    (:types 
        place locatable - object
        depot distributor - place
        truck hoist surface - locatable
        pallet crate - surface
        dead_end  ; Added type for dead ends
    )
    (:predicates
        (at ?x - locatable ?y - place)
        (on ?x - crate ?y - surface)
        (in ?x - crate ?y - truck)
        (lifting ?x - hoist ?y - crate)
        (available ?x - hoist)
        (clear ?x - surface)
        (dead_end_path ?x - place ?y - dead_end)  ; Added predicate for dead end paths
    )
    (:functions
        (distance ?x - place ?y - place)
        (speed ?t - truck)
        (weight ?c - crate)
        (power ?h - hoist)
    )
    ; ... (Rest of the domain actions remain the same)
)""")
    print(f"Depot domain file generated: {domain_file}")

def generate_depot_problem_pddl(num_places, num_dead_ends, num_trucks, num_hoists, num_crates, problem_file):
    depots = [f"depot{i}" for i in range(num_places)]
    distributors = [f"distributor{i}" for i in range(num_places)]
    dead_ends = [f"dead_end{i}" for i in range(1, num_dead_ends + 1)]
    trucks = [f"truck{i}" for i in range(num_trucks)]
    hoists = [f"hoist{i}" for i in range(num_hoists)]
    crates = [f"crate{i}" for i in range(num_crates)]
    pallets = [f"pallet{i}" for i in range(num_crates)]  # Assuming one pallet per crate for simplicity
    places = depots + distributors

    with open(problem_file, "w") as file:
        file.write("(define (problem depotprob) (:domain Depot)\n")
        file.write("  (:objects\n    ")
        file.write(" ".join(depots) + " - depot\n    ")
        file.write(" ".join(distributors) + " - distributor\n    ")
        file.write(" ".join(dead_ends) + " - dead_end\n    ")
        file.write(" ".join(trucks) + " - truck\n    ")
        file.write(" ".join(hoists) + " - hoist\n    ")
        file.write(" ".join(crates) + " - crate\n    ")
        file.write(" ".join(pallets) + " - pallet\n  )\n")
        file.write("  (:init\n")

        # Initialize trucks, hoists, crates, and dead ends
        for truck in trucks:
            file.write(f"    (at {truck} {random.choice(places)})\n")
            file.write(f"    (= (speed {truck}) {random.randint(1, 5)})\n")
        for hoist in hoists:
            file.write(f"    (at {hoist} {random.choice(places)})\n")
            file.write(f"    (available {hoist})\n")
            file.write(f"    (= (power {hoist}) {random.randint(1, 10)})\n")
        for i, crate in enumerate(crates):
            pallet = pallets[i]
            place = random.choice(places)
            file.write(f"    (at {crate} {place})\n")
            file.write(f"    (at {pallet} {place})\n")
            file.write(f"    (on {crate} {pallet})\n")
            file.write(f"    (clear {crate})\n")
            file.write(f"    (= (weight {crate}) {random.randint(10, 100)})\n")
        for place1 in places:
            for place2 in places:
                distance = random.randint(1, 10) if place1 != place2 else 0
                file.write(f"    (= (distance {place1} {place2}) {distance})\n")
        for place in places:
            dead_end_conn = random.choice(dead_ends)
            file.write(f"    (dead_end_path {place} {dead_end_conn})\n")

        file.write("  )\n")
        file.write("  (:goal\n    (and\n")
        # Define some example goal conditions
        file.write("    (on crate0 crate1)\n")
        file.write("    (on crate2 pallet0)\n")
        file.write("    )\n  )\n")
        file.write("  (:metric minimize (total-time))\n")
        file.write(")\n")

    print(f"Depot problem file generated: {problem_file}")


# Generate depot domain and problem files
generate_depot_domain_pddl("domain.pddl")
# Example usage
generate_depot_problem_pddl(3, 5, 2, 3, 5, "pfile1")
