
(define (problem car_route)
  (:domain autonomous_car)

  (:objects 
    car1 - car
    loc1 loc2 loc3 loc4 - location
  )

  (:init 
    (car_at car1 loc1)
    (truck_at loc3)
    (fuel_level car1 high)
    (road_between loc1 loc2) (road_between loc1 loc3) (road_between loc1 loc4) (road_between loc2 loc1) (road_between loc2 loc3) (road_between loc2 loc4) (road_between loc3 loc1) (road_between loc3 loc2) (road_between loc3 loc4) (road_between loc4 loc1) (road_between loc4 loc2) (road_between loc4 loc3)
    (traffic loc1 low) (traffic loc2 medium) (traffic loc3 medium) (traffic loc4 low)
    (truck_behavior close)
    (= (battery_level car1) 100)
  )

  (:goal 
    (and (car_at car1 loc4)
         (not (truck_behavior cut_into)))
  )
)
