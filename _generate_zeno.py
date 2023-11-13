import random

def generate_pddl_problem(num_cities, num_aircraft, num_people):
    # Create objects
    cities = [f"city{i}" for i in range(num_cities)]
    aircrafts = [f"plane{i}" for i in range(num_aircraft)]
    people = [f"person{i}" for i in range(num_people)]

    # Initial Conditions
    initial_conditions = []
    for i, plane in enumerate(aircrafts):
        city_index = random.randint(0, num_cities - 1)
        initial_conditions.append(f"(at {plane} {cities[city_index]})")
        initial_fuel = random.randint(100, 500)  # More restrictive fuel levels
        initial_conditions.append(f"(= (fuel {plane}) {initial_fuel})")

    for i, person in enumerate(people):
        city_index = random.randint(0, num_cities - 1)
        initial_conditions.append(f"(at {person} {cities[city_index]})")
        initial_conditions.append(f"(still-on-time {person})")

    # Distances between cities - more variability
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance = random.randint(100, 1000)  # Randomized distances
                initial_conditions.append(f"(= (distance city{i} city{j}) {distance})")

    # Goals - more complex
    goals = []
    for i, person in enumerate(people):
        target_city = cities[random.randint(0, num_cities - 1)]
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
num_cities = 15  # Increased number of cities
num_aircraft = 10  # Increased number of aircraft
num_people = 20  # Increased number of people

problem_content = generate_pddl_problem(num_cities, num_aircraft, num_people)

# Write to a file
with open("pfile1", "w") as file:
    file.write(problem_content)

print("PDDL Problem file generated: pfile1")
