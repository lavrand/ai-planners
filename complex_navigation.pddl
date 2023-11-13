(define (domain complex_navigation)
    (:requirements :strips :typing)
    (:types
        location
        dead_end  ; New type for dead ends
    )
    (:predicates
        (path ?from - location ?to - location)
        (dead_end_path ?from - location ?to - dead_end) ; Paths leading to dead ends
        (at ?loc - location)
    )
    (:action move
        :parameters (?from ?to - location)
        :precondition (and (at ?from) (path ?from ?to))
        :effect (and (not (at ?from)) (at ?to))
    )
    (:action move_to_dead_end
        :parameters (?from - location ?to - dead_end)
        :precondition (and (at ?from) (dead_end_path ?from ?to))
        :effect (and (not (at ?from))) ; The agent moves but doesn't reach a valid location
    )
)
