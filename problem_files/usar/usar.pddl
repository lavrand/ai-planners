(define (domain usar)
  (:requirements :strips :typing :durative-actions :fluents)
  (:types robot victim debris area)

  (:functions
    (battery-level ?r - robot) ; Battery level of robots
    (debris-weight ?d - debris) ; Weight of debris pieces
    (rescue-time ?v - victim) ; Time required to rescue a victim
  )

  (:predicates
    (robot-at ?r - robot ?a - area)
    (victim-at ?v - victim ?a - area)
    (debris-at ?d - debris ?a - area)
    (path-clear ?from ?to - area)
    (rescued ?v - victim)
    (robot-functional ?r - robot)
  )

  (:durative-action move
    :parameters (?r - robot ?from ?to - area)
    :duration (= ?duration (* 0.5 (distance ?from ?to))) ; Duration based on distance
    :condition (and (at start (robot-at ?r ?from)) (over all (path-clear ?from ?to)) (over all (robot-functional ?r)))
    :effect (and (at start (not (robot-at ?r ?from))) (at end (robot-at ?r ?to)) (at end (decrease (battery-level ?r) (* 0.1 (distance ?from ?to)))))
  )

  (:durative-action clear-debris
    :parameters (?r - robot ?d - debris ?a - area)
    :duration (= ?duration (* 2 (debris-weight ?d)))
    :condition (and (at start (robot-at ?r ?a)) (over all (debris-at ?d ?a)) (over all (robot-functional ?r)))
    :effect (and (at end (not (debris-at ?d ?a))) (at end (decrease (battery-level ?r) (* 0.2 (debris-weight ?d)))))
  )

  (:durative-action rescue-victim
    :parameters (?r - robot ?v - victim ?a - area)
    :duration (= ?duration (rescue-time ?v))
    :condition (and (at start (robot-at ?r ?a)) (over all (victim-at ?v ?a)) (over all (robot-functional ?r)))
    :effect (and (at end (rescued ?v)) (at end (decrease (battery-level ?r) 5)))
  )

  (:durative-action recharge-robot
    :parameters (?r - robot)
    :duration (= ?duration 10)
    :condition (at start (robot-functional ?r))
    :effect (at end (increase (battery-level ?r) 20))
  )
)
