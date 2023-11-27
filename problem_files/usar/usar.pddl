(define (domain usar)
  (:requirements :strips :typing :durative-actions)
  (:types robot victim debris area)

  (:predicates
    (robot-at ?r - robot ?a - area)
    (victim-at ?v - victim ?a - area)
    (debris-at ?d - debris ?a - area)
    (path-clear ?from ?to - area)
    (rescued ?v - victim)
  )

  (:durative-action move
    :parameters (?r - robot ?from ?to - area)
    :duration (= ?duration 5)
    :condition (and (at start (robot-at ?r ?from)) (over all (path-clear ?from ?to)))
    :effect (and (at start (not (robot-at ?r ?from))) (at end (robot-at ?r ?to)))
  )

  (:durative-action clear-debris
    :parameters (?r - robot ?d - debris ?a - area)
    :duration (= ?duration 10)
    :condition (and (at start (robot-at ?r ?a)) (over all (debris-at ?d ?a)))
    :effect (at end (not (debris-at ?d ?a)))
  )

  (:durative-action rescue-victim
    :parameters (?r - robot ?v - victim ?a - area)
    :duration (= ?duration 15)
    :condition (and (at start (robot-at ?r ?a)) (over all (victim-at ?v ?a)))
    :effect (at end (rescued ?v))
  )
)
