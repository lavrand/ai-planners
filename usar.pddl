(define (domain usar)
  (:requirements :strips :typing :durative-actions :fluents :timed-initial-literals)
  (:types robot victim debris area task)

  (:functions
    (battery-level ?r - robot)
    (task-duration ?t - task)
    (distance ?from ?to - area)
  )

  (:predicates
    (robot-at ?r - robot ?a - area)
    (task-at ?t - task ?a - area)
    (debris-at ?d - debris ?a - area)
    (task-completed ?t - task)
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
