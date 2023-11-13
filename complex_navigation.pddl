(define (domain complex_navigation)
  (:requirements :strips :typing)
  (:types location)
  (:predicates
    (at ?l - location)
    (path ?from ?to - location)
  )

  (:action move
    :parameters (?from ?to - location)
    :precondition (and (at ?from) (path ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
)
