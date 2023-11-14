(define (domain autonomous_car)
  (:requirements :strips :typing)
  (:types location car)

  (:predicates
    (car_at ?car - car ?location - location)
    (truck_at ?location - location)
    (road_between ?from - location ?to - location)
    (fuel_level ?car - car ?level - (either low medium high))
    (distance_to_truck ?car - car ?dist - (either safe close very_close))
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
)
