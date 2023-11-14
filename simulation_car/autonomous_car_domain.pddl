(define (domain autonomous_car)
  (:requirements :strips :typing :durative-actions :fluents :adl :negative-preconditions :duration-inequalities)
  (:types
    location car
  )

  (:predicates
    (car_at ?car - car ?location - location)
    (road_between ?from - location ?to - location)
    (fuel_level ?car - car ?level - (either low medium high))
    (traffic ?location - location ?level - (either low medium high))
    (truck_at ?location - location)
    (truck_behavior ?behavior - (either safe close very_close cut_into))
  )

  (:functions
    (battery_level ?car - car)
  )

  (:durative-action drive
    :parameters (?car - car ?from ?to - location)
    :duration (>= ?duration 5)
    :condition (and
                 (over all (car_at ?car ?from))
                 (over all (road_between ?from ?to))
                 (at start (fuel_level ?car high))
                 (at start (traffic ?to low)))
    :effect (and
              (at start (decrease (battery_level ?car) 10))
              (at end (not (car_at ?car ?from)))
              (at end (car_at ?car ?to)))
  )

  (:durative-action avoid_truck
    :parameters (?car - car ?from ?to - location)
    :duration (= ?duration 1)
    :condition (and
                 (over all (car_at ?car ?from))
                 (over all (road_between ?from ?to))
                 (at start (truck_at ?to))
                 (at start (truck_behavior very_close)))
    :effect (and
              (at end (not (truck_at ?to)))
              (at end (not (truck_behavior very_close)))
              (at end (truck_behavior safe)))
  )

  (:durative-action wait
    :parameters (?car - car ?location - location)
    :duration (>= ?duration 1)
    :condition (and
                 (over all (car_at ?car ?location))
                 (over all (traffic ?location high)))
    :effect (and
              (at start (decrease (battery_level ?car) 2)))
  )

  (:durative-action charge
    :parameters (?car - car ?location - location)
    :duration (= ?duration 10)
    :condition (and
                 (over all (car_at ?car ?location)))
    :effect (and
              (at end (increase (battery_level ?car) 50)))
  )
)
