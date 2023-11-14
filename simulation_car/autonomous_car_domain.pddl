(define (domain autonomous_car)
  (:requirements :strips :typing :disjunctive-preconditions)
  (:types
    location car fuel_level distance
  )

  (:constants
    high medium low - fuel_level
    safe close very_close cut_into - distance
  )

  (:predicates
    (car_at ?car - car ?location - location)
    (truck_at ?location - location)
    (road_between ?from - location ?to - location)
    (fuel_level ?car - car ?level - fuel_level)
    (distance_to_truck ?car - car ?dist - distance)
  )

  (:action move
    :parameters (?car - car ?from - location ?to - location)
    :precondition (and (car_at ?car ?from) (road_between ?from ?to) (fuel_level ?car high) (or (distance_to_truck ?car safe) (distance_to_truck ?car close)))
    :effect (and (not (car_at ?car ?from)) (car_at ?car ?to) (distance_to_truck ?car safe))
  )

  (:action avoid_truck
    :parameters (?car - car ?from - location ?to - location)
    :precondition (and (car_at ?car ?from) (road_between ?from ?to) (distance_to_truck ?car very_close))
    :effect (and (not (car_at ?car ?from)) (car_at ?car ?to) (distance_to_truck ?car safe))
  )

  (:action refuel
    :parameters (?car - car)
    :precondition (fuel_level ?car low)
    :effect (fuel_level ?car high)
  )

  ;; Define additional actions related to 'cut_into' behavior here if necessary
)
