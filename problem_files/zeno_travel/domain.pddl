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
        )
    )

    (:durative-action fly
        :parameters (?a - aircraft ?c1 ?c2 - city)
        :duration (= ?duration (/ (distance ?c1 ?c2) (slow-speed ?a)))
        :condition (and
            (at start (at ?a ?c1))
            (at start (>= (fuel ?a) (* (distance ?c1 ?c2) (slow-burn ?a))))
        )
        :effect (and
            (at start (not (at ?a ?c1)))
            (at end (at ?a ?c2))
            (at end (increase (total-fuel-used) (* (distance ?c1 ?c2) (slow-burn ?a))))
            (at end (decrease (fuel ?a) (* (distance ?c1 ?c2) (slow-burn ?a))))
            ; Assuming that flying may affect the on-time status based on some criteria
            (forall (?p - person)
                (when (in ?p ?a)
                    ; Here you might want to include conditions under which a person remains or does not remain "on time"
                    ; This example assumes they're no longer on time if they fly slowly
                    (not (still-on-time ?p))
                )
            )
        )
    )

    (:durative-action zoom
        :parameters (?a - aircraft ?c1 ?c2 - city)
        :duration (= ?duration (/ (distance ?c1 ?c2) (fast-speed ?a)))
        :condition (and
            (at start (at ?a ?c1))
            (at start (>= (fuel ?a) (* (distance ?c1 ?c2) (fast-burn ?a))))
        )
        :effect (and
            (at start (not (at ?a ?c1)))
            (at end (at ?a ?c2))
            (at end (increase (total-fuel-used) (* (distance ?c1 ?c2) (fast-burn ?a))))
            (at end (decrease (fuel ?a) (* (distance ?c1 ?c2) (fast-burn ?a))))
            ; Zooming might improve the chances of remaining on time due to faster travel
            (forall (?p - person)
                (when (in ?p ?a)
                    ; Similar to flying, you need specific conditions here. We assume they're still on time if they zoom.
                    (still-on-time ?p)
                )
            )
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
        )
    )
)
