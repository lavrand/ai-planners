(define (domain complex_navigation)
    (:requirements :strips :typing :equality :negative-preconditions)
    (:types 
        location
        dead_end
        key
    )
    (:predicates
        (path ?from - location ?to - location)
        (dead_end_path ?from - location ?to - dead_end)
        (at ?loc - location)
        (key_at ?key - key ?loc - location)
        (has_key)
        (visited ?loc - location)  ; Declare visited predicate
    )
    (:action move
        :parameters (?from ?to - location)
        :precondition (and (at ?from) (path ?from ?to) (not (visited ?to)))
        :effect (and (not (at ?from)) (at ?to) (visited ?to))
    )
    (:action move_to_dead_end
        :parameters (?from - location ?to - dead_end)
        :precondition (and (at ?from) (dead_end_path ?from ?to))
        :effect (and (not (at ?from)))
    )
    (:action pick_up_key
        :parameters (?key - key ?loc - location)
        :precondition (and (at ?loc) (key_at ?key ?loc) (not (has_key)))
        :effect (has_key)
    )
)