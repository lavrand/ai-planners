(define (domain zeno-travel)
    (:requirements :durative-actions :typing :fluents)
    (:types aircraft person city - object)

    (:predicates
        (at ?x - (either person aircraft) ?c - city)
        (in ?p - person ?a - aircraft)
        (still-on-time ?p - person)  ; Predicate to determine if a person is still on time
    )

    (:functions
        (fuel ?a - aircraft)
        (distance ?c1 - city ?c2 - city)
        (slow-speed ?a - aircraft)
        (fast-speed ?a - aircraft)
        (slow-burn ?a - aircraft)
        (fast-burn ?a - aircraft)
        (capacity ?a - aircraft)
        (refuel-rate ?a - aircraft)
        (total-fuel-used)
        (boarding-time)
        (debarking-time)
        (deadline ?p - person)  ; Assuming a deadline is set for each person's journey
    )

    (:durative-action board
        :parameters (?p - person ?a - aircraft ?c - city)
        :duration (= ?duration (boarding-time))
        :condition (and
            (at start (at ?p ?c))
            (over all (at ?a ?c))
            (at start (still-on-time ?p))  ; Check if the person is still on time
        )
        :effect (and
            (at start (not (at ?p ?c)))
            (at end (in ?p ?a))
            ; We assume boarding does not affect the on-time status.
        )
    )

    (:durative-action debark
        :parameters (?p - person ?a - aircraft ?c - city)
        :duration (= ?duration (debarking-time))
        :condition (and
            (at start (in ?p ?a))
            (over all (at ?a ?c))
            (at start (still-on-time ?p))  ; Check if the person is still on time
        )
        :effect (and
            (at start (not (in ?p ?a)))
            (at end (at ?p ?c))
            ; We assume debarking does not affect the on-time status.
        )
    )

    (:durative-action fly
        :parameters (?a - aircraft ?c1 ?c2 - city ?p - person)
        :duration (= ?duration (/ (distance ?c1 ?c2) (slow-speed ?a)))
        :condition (and
            (at start (at ?a ?c1))
            (at start (>= (fuel ?a) (* (distance ?c1 ?c2) (slow-burn ?a))))
            (at start (in ?p ?a))  ; the person must be in the aircraft
            (at start (still-on-time ?p))  ; the person is initially still on time
        )
        :effect (and
            (at start (not (at ?a ?c1)))
            (at end (at ?a ?c2))
            (at end (increase (total-fuel-used) (* (distance ?c1 ?c2) (slow-burn ?a))))
            (at end (decrease (fuel ?a) (* (distance ?c1 ?c2) (slow-burn ?a))))
            (at end (not (still-on-time ?p)))  ; the person is no longer on time after flying
        )
    )

    (:durative-action zoom
        :parameters (?a - aircraft ?c1 ?c2 - city ?p - person)
        :duration (= ?duration (/ (distance ?c1 ?c2) (fast-speed ?a)))
        :condition (and
            (at start (at ?a ?c1))
            (at start (>= (fuel ?a) (* (distance ?c1 ?c2) (fast-burn ?a))))
            (at start (in ?p ?a))  ; the person must be in the aircraft
            (at start (not (still-on-time ?p)))  ; the person is initially not on time
        )
        :effect (and
            (at start (not (at ?a ?c1)))
            (at end (at ?a ?c2))
            (at end (increase (total-fuel-used) (* (distance ?c1 ?c2) (fast-burn ?a))))
            (at end (decrease (fuel ?a) (* (distance ?c1 ?c2) (fast-burn ?a))))
            (at end (still-on-time ?p))  ; the person is now on time after zooming
        )
    )



    (:durative-action refuel
        :parameters (?a - aircraft ?c - city)
        :duration (= ?duration (/ (- (capacity ?a) (fuel ?a)) (refuel-rate ?a)))
        :condition (and
            (at start (> (capacity ?a) (fuel ?a)))
            (over all (at ?a ?c))
        )
        :effect (and
            (at end (assign (fuel ?a) (capacity ?a)))
            ; Refueling might be a neutral action regarding time status. It neither improves nor worsens the on-time condition.
        )
    )
)
