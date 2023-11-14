
(define (domain dynamic_rescue)
    (:requirements :strips :typing)
    (:types location - object)
    (:predicates
        (robot_at ?loc - location)
        (target_at ?loc - location)
        (obstacle_at ?loc - location)
        (rescued ?loc - location)
    )
    (:action move
        :parameters (?from ?to - location)
        :precondition (and (robot_at ?from) (not (obstacle_at ?to)))
        :effect (and (not (robot_at ?from)) (robot_at ?to))
    )
    (:action scan_for_target
        :parameters (?loc - location)
        :precondition (robot_at ?loc)
        :effect (when (target_at ?loc) (rescued ?loc))
    )
)
