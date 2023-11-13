import random

def generate_pddl_problem(num_cities, num_aircraft, num_people):
    # Create objects
    cities = [f"city{i}" for i in range(num_cities)]
    aircrafts = [f"plane{i}" for i in range(num_aircraft)]
    people = [f"person{i}" for i in range(num_people)]

    # Initial Conditions
    initial_conditions = []
    city_aircraft_map = {}

    # Assigning aircrafts to cities and setting fuel
    for plane in aircrafts:
        city_index = random.randint(0, num_cities - 1)
        city_aircraft_map.setdefault(city_index, []).append(plane)
        initial_conditions.append(f"(at {plane} {cities[city_index]})")
        initial_fuel = random.randint(500, 1000)  # Ensuring adequate fuel
        initial_conditions.append(f"(= (fuel {plane}) {initial_fuel})")

    # Assigning people to cities with at least one aircraft
    for person in people:
        city_index = random.choice(list(city_aircraft_map.keys()))
        initial_conditions.append(f"(at {person} {cities[city_index]})")
        initial_conditions.append(f"(still-on-time {person})")

    # Distances between cities
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance = random.randint(100, 1000)
                initial_conditions.append(f"(= (distance city{i} city{j}) {distance})")

    # Goals - ensuring at least one achievable goal for each person
    goals = []
    for person in people:
        available_cities = list(set(range(num_cities)) - {city_index})
        target_city = cities[random.choice(available_cities)]
        goals.append(f"(at {person} {target_city})")

    # Generate problem file content
    problem_content = f"""
(define (problem complex-travel)
  (:domain zeno-travel)
  (:objects
    {' '.join(cities)} - city
    {' '.join(aircrafts)} - aircraft
    {' '.join(people)} - person
  )
  (:init
    {' '.join(initial_conditions)}
  )
  (:goal (and
    {' '.join(goals)}
  ))
  (:metric minimize (+ (* 1 (total-time))  (* 0.005 (total-fuel-used))))
)
"""
    return problem_content

# Generate the problem file content
num_cities = 15
num_aircraft = 10
num_people = 20

problem_content = generate_pddl_problem(num_cities, num_aircraft, num_people)

# Write to a file
with open("pfile1", "w") as file:
    file.write(problem_content)

print("PDDL Problem file generated: pfile1")
