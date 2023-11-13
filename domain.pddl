(define (domain Depot)
    (:requirements :typing :durative-actions :fluents)
    (:types 
        place locatable - object
        depot distributor - place
        truck hoist surface - locatable
        pallet crate - surface
        dead_end  ; Added type for dead ends
    )
    (:predicates
        (at ?x - locatable ?y - place)
        (on ?x - crate ?y - surface)
        (in ?x - crate ?y - truck)
        (lifting ?x - hoist ?y - crate)
        (available ?x - hoist)
        (clear ?x - surface)
        (dead_end_path ?x - place ?y - dead_end)  ; Added predicate for dead end paths
    )
    (:functions
        (distance ?x - place ?y - place)
        (speed ?t - truck)
        (weight ?c - crate)
        (power ?h - hoist)
    )
    ; ... (Rest of the domain actions remain the same)
)