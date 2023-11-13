def generate_pddl_problem(num_cities, num_aircraft, num_people):
    # Create objects
    cities = [f"city{i}" for i in range(num_cities)]
    aircrafts = [f"plane{i}" for i in range(num_aircraft)]
    people = [f"person{i}" for i in range(num_people)]

    # Initial Conditions
    initial_conditions = []
    for i, plane in enumerate(aircrafts):
        initial_conditions.append(f"(at {plane} {cities[i % num_cities]})")
        initial_conditions.append(f"(= (fuel {plane}) 500)")  # Example fuel level

    for i, person in enumerate(people):
        initial_conditions.append(f"(at {person} {cities[i % num_cities]})")
        initial_conditions.append(f"(still-on-time {person})")  # Added this line

    # Distances between cities
    for i in range(num_cities):
        for j in range(num_cities):
            distance = abs(i - j) * 100  # Example distance calculation
            initial_conditions.append(f"(= (distance city{i} city{j}) {distance})")

    # Goals
    goals = []
    for person in people:
        target_city = cities[int(person[-1]) % num_cities]  # Example goal assignment
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
num_cities = 10  # Number of cities
num_aircraft = 5  # Number of aircraft
num_people = 15  # Number of people

problem_content = generate_pddl_problem(num_cities, num_aircraft, num_people)

# Write to a file
with open("pfile1", "w") as file:
    file.write(problem_content)

print("PDDL Problem file generated: zeno_travel_problem.pddl")
