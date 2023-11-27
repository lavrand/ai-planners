(define (domain usar)
  (:requirements :strips :typing :durative-actions :fluents :timed-initial-literals)
  (:types robot victim debris area)

  (:functions
    (battery-level ?r - robot)
    (distance ?from ?to - area)
  )

  (:predicates
    (robot-at ?r - robot ?a - area)
    (victim-at ?v - victim ?a - area)           ; Declare victim-at predicate
    (debris-at ?d - debris ?a - area)
    (victim-rescued ?v - victim)                ; Declare victim-rescued predicate
    (debris-cleared ?d - debris)                ; Declare debris-cleared predicate
    (robot-functional ?r - robot)
  )

  (:durative-action move
    :parameters (?r - robot ?from ?to - area)
    :duration (= ?duration (distance ?from ?to))
    :condition (and (at start (robot-at ?r ?from)) (over all (robot-functional ?r)))
    :effect (and (at start (not (robot-at ?r ?from))) (at end (robot-at ?r ?to)))
  )

  (:durative-action perform-task
    :parameters (?r - robot ?t - task ?a - area)
    :duration (= ?duration (task-duration ?t))
    :condition (and (at start (robot-at ?r ?a)) (at start (task-at ?t ?a)) (over all (robot-functional ?r)))
    :effect (at end (task-completed ?t))
  )

  (:durative-action clear-debris
    :parameters (?r - robot ?d - debris ?a - area)
    :duration (= ?duration 10)
    :condition (and (at start (robot-at ?r ?a)) (over all (debris-at ?d ?a)) (over all (robot-functional ?r)))
    :effect (at end (not (debris-at ?d ?a)))
  )
)
