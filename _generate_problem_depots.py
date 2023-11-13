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
        (still-on-time ?x - crate) ;; added by AIC: it's still 'on time' to achieve the goal (on ?x ...) for the crate ?x

    )
    (:functions
        (distance ?x - place ?y - place)
        (speed ?t - truck)
        (weight ?c - crate)
        (power ?h - hoist)
    )
    (:durative-action Drive
    :parameters (?x - truck ?y - place ?z - place) 
    :duration (= ?duration (/ (distance ?y ?z) (speed ?x)))
    :condition (and (at start (at ?x ?y)) (at start (not (= ?y ?z))))
    :effect (and (at start (not (at ?x ?y))) (at end (at ?x ?z))))
    
    (:durative-action Lift
    :parameters (?x - hoist ?y - crate ?z - surface ?p - place)
    :duration (= ?duration 1)
    :condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (available ?x)) (at start (at ?y ?p)) (over all (still-on-time ?y)) (at start (on ?y ?z)) (at start (clear ?y)))
    :effect (and (at start (not (at ?y ?p))) (at end (lifting ?x ?y)) (at start (not (clear ?y))) (at start (not (available ?x))) 
                 (at end (clear ?z)) (at start (not (on ?y ?z)))))
    
    (:durative-action Drop 
    :parameters (?x - hoist ?y - crate ?z - surface ?p - place)
    :duration (= ?duration 1)
    :condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (clear ?z)) (at start (lifting ?x ?y))  (over all (still-on-time ?y)))
    :effect (and (at end (available ?x)) (at start (not (lifting ?x ?y))) (at end (at ?y ?p)) (at start (not (clear ?z))) (at end (clear ?y))
            (at end (on ?y ?z))))
    
    (:durative-action Load
    :parameters (?x - hoist ?y - crate ?z - truck ?p - place)
    :duration (= ?duration (/ (weight ?y) (power ?x)))
    :condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (lifting ?x ?y)) (over all (still-on-time ?y)) )
    :effect (and (at start (not (lifting ?x ?y))) (at end (in ?y ?z)) (at end (available ?x))))
    
    (:durative-action Unload 
    :parameters (?x - hoist ?y - crate ?z - truck ?p - place)
    :duration (= ?duration (/ (weight ?y) (power ?x)))
    :condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (available ?x)) (at start (in ?y ?z)) (over all (still-on-time ?y)) )
    :effect (and (at start (not (in ?y ?z))) (at start (not (available ?x))) (at end (lifting ?x ?y))))
    
    )
    """)
    print(f"Depot domain file generated: {domain_file}")

def generate_depot_problem_pddl(num_places, num_dead_ends, num_trucks, num_hoists, num_crates, problem_file):
    depots = [f"depot{i}" for i in range(num_places)]
    distributors = [f"distributor{i}" for i in range(num_places)]
    dead_ends = [f"dead_end{i}" for i in range(1, num_dead_ends + 1)]
    trucks = [f"truck{i}" for i in range(num_trucks)]
    hoists = [f"hoist{i}" for i in range(num_hoists)]
    crates = [f"crate{i}" for i in range(num_crates)]
    pallets = [f"pallet{i}" for i in range(num_crates)]  # Assuming one pallet per crate for simplicity

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

        # Initialize locations of trucks, hoists, crates, and dead ends
        for truck in trucks:
            file.write(f"    (at {truck} {random.choice(depots)})\n")
            file.write(f"    (= (speed {truck}) {random.randint(1, 5)})\n")
        for hoist in hoists:
            file.write(f"    (at {hoist} {random.choice(depots)})\n")
            file.write(f"    (available {hoist})\n")
            file.write(f"    (= (power {hoist}) {random.randint(1, 10)})\n")
        for i, crate in enumerate(crates):
            pallet = pallets[i]
            place = random.choice(depots + distributors)
            file.write(f"    (at {crate} {place})\n")
            file.write(f"    (on {crate} {pallet})\n")
            file.write(f"    (= (weight {crate}) {random.randint(10, 100)})\n")
        for place in depots + distributors:
            for other_place in depots + distributors:
                distance = random.randint(1, 10) if place != other_place else 0
                file.write(f"    (= (distance {place} {other_place}) {distance})\n")
        for place in depots + distributors:
            dead_end_conn = random.choice(dead_ends)
            file.write(f"    (dead_end_path {place} {dead_end_conn})\n")
        file.write("  )\n")
        file.write("  (:goal\n    (and\n")

        # Define some example goal conditions
        for i in range(min(4, num_crates)):  # Example goal: moving up to 4 crates
            target = random.choice(depots + distributors)
            file.write(f"        (at crate{i} {target})\n")
        file.write("    )\n  )\n")
        file.write("  (:metric minimize (total-time))\n")
        file.write(")\n")

    print(f"Depot problem file generated: {problem_file}")


# Generate depot domain and problem files
generate_depot_domain_pddl("domain.pddl")
# Example usage
generate_depot_problem_pddl(3, 5, 2, 3, 5, "pfile1")
