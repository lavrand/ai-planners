(define (domain Depot)
(:requirements :typing :durative-actions :fluents)
(:types place locatable - object
	depot distributor - place
        truck hoist surface - locatable
        pallet crate - surface)

(:predicates (at ?x - locatable ?y - place) 
             (on ?x - crate ?y - surface)
             (in ?x - crate ?y - truck)
             (lifting ?x - hoist ?y - crate)
             (available ?x - hoist)
             (clear ?x - surface)
             (still-on-time ?x - crate) ;; added by AIC: it's still 'on time' to achieve the goal (on ?x ...) for the crate ?x
)

(:functions (distance ?x - place ?y - place)
	    (speed ?t - truck)
	    (weight ?c - crate)
	    (power ?h - hoist))
	
(:durative-action Drive
:parameters (?x - truck ?y - place ?z - place) 
:duration (= ?duration (/ (distance ?y ?z) (speed ?x)))
:condition (and (at start (at ?x ?y)) (at start (not (= ?y ?z))))
:effect (and (at start (not (at ?x ?y))) (at end (at ?x ?z))))

(:durative-action Lift
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:duration (= ?duration 1)
:condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (available ?x)) (at start (at ?y ?p)) (over all (still-on-time ?y)) (at start (on ?y ?z)) (at start (clear ?y)))
:effect (and (at start (not (at ?y ?p))) (at end (lifting ?x ?y)) (at start (not (clear ?y))) (at start (not (available ?x))) 
             (at end (clear ?z)) (at start (not (on ?y ?z)))))

(:durative-action Drop 
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:duration (= ?duration 1)
:condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (clear ?z)) (at start (lifting ?x ?y))  (over all (still-on-time ?y)))
:effect (and (at end (available ?x)) (at start (not (lifting ?x ?y))) (at end (at ?y ?p)) (at start (not (clear ?z))) (at end (clear ?y))
		(at end (on ?y ?z))))

(:durative-action Load
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:duration (= ?duration (/ (weight ?y) (power ?x)))
:condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (lifting ?x ?y)) (over all (still-on-time ?y)) )
:effect (and (at start (not (lifting ?x ?y))) (at end (in ?y ?z)) (at end (available ?x))))

(:durative-action Unload 
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:duration (= ?duration (/ (weight ?y) (power ?x)))
:condition (and (over all (at ?x ?p)) (over all (at ?z ?p)) (at start (available ?x)) (at start (in ?y ?z)) (over all (still-on-time ?y)) )
:effect (and (at start (not (in ?y ?z))) (at start (not (available ?x))) (at end (lifting ?x ?y))))

)
