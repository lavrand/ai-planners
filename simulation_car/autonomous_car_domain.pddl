(define (domain autonomous_car)
  (:requirements :strips :typing :durative-actions :fluents :adl :negative-preconditions :duration-inequalities)

  (:types
    location
    car
    fuel_level truck_state - enumeration
  )

  (:constants
    high medium low - fuel_level
    safe close very_close cut_into - truck_state
  )

  (:predicates
    (car_at ?car - car ?location - location)
    (road_between ?from - location ?to - location)
    (traffic ?location - location ?level - fuel_level)
    (truck_at ?location - location)
    (truck_behavior ?behavior - truck_state)
  )

  (:functions
    (battery_level ?car - car)
  )

  (:durative-action drive
    :parameters (?car - car ?from - location ?to - location)
    :duration (= ?duration 5)
    :condition (and
                 (over all (car_at ?car ?from))
                 (over all (road_between ?from ?to))
                 (at start (not (traffic ?to high)))
                 (at start (not (truck_behavior cut_into))))
    :effect (and
              (at start (decrease (battery_level ?car) 10))
              (at end (not (car_at ?car ?from)))
              (at end (car_at ?car ?to)))
  )

  (:durative-action change_traffic
    :parameters (?location - location ?new_level - fuel_level)
    :duration (= ?duration 1)
    :condition (and)
    :effect (and
              (at end (traffic ?location ?new_level)))
  )

  (:durative-action react_to_truck
    :parameters (?car - car ?location - location)
    :duration (= ?duration 1)
    :condition (and
                 (over all (car_at ?car ?location))
                 (over all (truck_at ?location))
                 (over all (truck_behavior very_close)))
    :effect (and
              (at end (not (truck_behavior very_close)))
              (at end (truck_behavior safe)))
  )

  (:action refuel
    :parameters (?car - car)
    :precondition (fuel_level ?car low)
    :effect (and
              (not (fuel_level ?car low))
              (fuel_level ?car high))
  )

  (:durative-action charge_battery
    :parameters (?car - car ?location - location)
    :duration (= ?duration 10)
    :condition (over all (car_at ?car ?location))
    :effect (at end (increase (battery_level ?car) 50))
  )

  ;; Additional actions can be added as needed
)
