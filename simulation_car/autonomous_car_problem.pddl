(define (problem car_route)
  (:domain autonomous_car)
  (:objects
    car1 - car
    loc1 loc2 loc3 loc4 - location
  )

  (:init
    (car_at car1 loc1)
    (truck_at loc2)
    (fuel_level car1 high)
    (distance_to_truck car1 safe)
    (road_between loc1 loc2)
    (road_between loc2 loc3)
    (road_between loc3 loc4)
    (road_between loc4 loc1)
  )

  (:goal
    (and (car_at car1 loc4) (distance_to_truck car1 safe))
  )
)