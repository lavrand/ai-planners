(define (problem rcll-production-073-durative)
	(:domain rcll-production-durative)
    
  (:objects
    R-1 - robot
    R-2 - robot
    R-3 - robot
    o1 - order
    wp1 - workpiece
    cg1 cg2 cg3 cb1 cb2 cb3 - cap-carrier
    C-BS C-CS1 C-CS2 C-DS - mps
    CYAN - team-color
  )
   
  (:init (order-delivery-window-open o1) (at 152.882 (not (order-delivery-window-open o1))) (can-commit-for-ontime-delivery o1) (at 8.80 (not (can-commit-for-ontime-delivery o1)))
   (mps-type C-BS BS)
   (mps-type C-CS1 CS)
   (mps-type C-CS2 CS) 
   (mps-type C-DS DS)
   (location-free START INPUT)
   (location-free C-BS INPUT)
   (location-free C-BS OUTPUT)
   (location-free C-CS1 INPUT)
   (location-free C-CS1 OUTPUT)
   (location-free C-CS2 INPUT)
   (location-free C-CS2 OUTPUT)
   (location-free C-DS INPUT)
   (location-free C-DS OUTPUT)
   (cs-can-perform C-CS1 CS_RETRIEVE)
   (cs-can-perform C-CS2 CS_RETRIEVE)
   (cs-free C-CS1)
   (cs-free C-CS2)

   (wp-base-color wp1 BASE_NONE)
   (wp-cap-color wp1 CAP_NONE)
   (wp-ring1-color wp1 RING_NONE)
   (wp-ring2-color wp1 RING_NONE)
   (wp-ring3-color wp1 RING_NONE)
   (wp-unused wp1)
   (robot-waiting R-1)
   (robot-waiting R-2)
   (robot-waiting R-3)

   (mps-state C-BS IDLE)
   (mps-state C-CS1 IDLE)
   (mps-state C-CS2 IDLE)
   (mps-state C-DS IDLE)

   (wp-cap-color cg1 CAP_GREY)
   (wp-cap-color cg2 CAP_GREY)
   (wp-cap-color cg3 CAP_GREY)
   (wp-on-shelf cg1 C-CS1 LEFT)
   (wp-on-shelf cg2 C-CS1 MIDDLE)
   (wp-on-shelf cg3 C-CS1 RIGHT)

   (wp-cap-color cb1 CAP_BLACK)
   (wp-cap-color cb2 CAP_BLACK)
   (wp-cap-color cb3 CAP_BLACK)
   (wp-on-shelf cb1 C-CS2 LEFT)
   (wp-on-shelf cb2 C-CS2 MIDDLE)
   (wp-on-shelf cb3 C-CS2 RIGHT)
   (order-complexity o1 c0)
   (order-base-color o1 BASE_RED)
   (order-cap-color o1 CAP_GREY)
   (order-gate o1 GATE-3)



   (= (path-length C-BS INPUT C-BS OUTPUT) 2.299945)
   (= (path-length C-BS INPUT C-CS1 INPUT) 10.618277)
   (= (path-length C-BS INPUT C-CS1 OUTPUT) 11.168703)
   (= (path-length C-BS INPUT C-CS2 INPUT) 3.705226)
   (= (path-length C-BS INPUT C-CS2 OUTPUT) 2.579954)
   (= (path-length C-BS INPUT C-DS INPUT) 7.684929)
   (= (path-length C-BS INPUT C-DS OUTPUT) 6.578719)
   (= (path-length C-BS OUTPUT C-BS INPUT) 2.299945)
   (= (path-length C-BS OUTPUT C-CS1 INPUT) 12.829994)
   (= (path-length C-BS OUTPUT C-CS1 OUTPUT) 12.176642)
   (= (path-length C-BS OUTPUT C-CS2 INPUT) 5.916943)
   (= (path-length C-BS OUTPUT C-CS2 OUTPUT) 4.791671)
   (= (path-length C-BS OUTPUT C-DS INPUT) 8.162046)
   (= (path-length C-BS OUTPUT C-DS OUTPUT) 6.093978)
   (= (path-length C-CS1 INPUT C-BS INPUT) 10.618278)
   (= (path-length C-CS1 INPUT C-BS OUTPUT) 12.829994)
   (= (path-length C-CS1 INPUT C-CS1 OUTPUT) 3.831761)
   (= (path-length C-CS1 INPUT C-CS2 INPUT) 6.987794)
   (= (path-length C-CS1 INPUT C-CS2 OUTPUT) 8.395306)
   (= (path-length C-CS1 INPUT C-DS INPUT) 7.731475)
   (= (path-length C-CS1 INPUT C-DS OUTPUT) 10.289251)
   (= (path-length C-CS1 OUTPUT C-BS INPUT) 11.168703)
   (= (path-length C-CS1 OUTPUT C-BS OUTPUT) 12.176641)
   (= (path-length C-CS1 OUTPUT C-CS1 INPUT) 3.831761)
   (= (path-length C-CS1 OUTPUT C-CS2 INPUT) 7.555974)
   (= (path-length C-CS1 OUTPUT C-CS2 OUTPUT) 9.570748)
   (= (path-length C-CS1 OUTPUT C-DS INPUT) 5.644189)
   (= (path-length C-CS1 OUTPUT C-DS OUTPUT) 8.201966)
   (= (path-length C-CS2 INPUT C-BS INPUT) 3.705226)
   (= (path-length C-CS2 INPUT C-BS OUTPUT) 5.916943)
   (= (path-length C-CS2 INPUT C-CS1 INPUT) 6.987794)
   (= (path-length C-CS2 INPUT C-CS1 OUTPUT) 7.555975)
   (= (path-length C-CS2 INPUT C-CS2 OUTPUT) 2.886805)
   (= (path-length C-CS2 INPUT C-DS INPUT) 4.162674)
   (= (path-length C-CS2 INPUT C-DS OUTPUT) 6.489504)
   (= (path-length C-CS2 OUTPUT C-BS INPUT) 2.579955)
   (= (path-length C-CS2 OUTPUT C-BS OUTPUT) 4.791671)
   (= (path-length C-CS2 OUTPUT C-CS1 INPUT) 8.395306)
   (= (path-length C-CS2 OUTPUT C-CS1 OUTPUT) 9.570747)
   (= (path-length C-CS2 OUTPUT C-CS2 INPUT) 2.886805)
   (= (path-length C-CS2 OUTPUT C-DS INPUT) 6.177448)
   (= (path-length C-CS2 OUTPUT C-DS OUTPUT) 6.240150)
   (= (path-length C-DS INPUT C-BS INPUT) 7.684930)
   (= (path-length C-DS INPUT C-BS OUTPUT) 8.162046)
   (= (path-length C-DS INPUT C-CS1 INPUT) 7.731476)
   (= (path-length C-DS INPUT C-CS1 OUTPUT) 5.644191)
   (= (path-length C-DS INPUT C-CS2 INPUT) 4.162675)
   (= (path-length C-DS INPUT C-CS2 OUTPUT) 6.177448)
   (= (path-length C-DS INPUT C-DS OUTPUT) 3.342637)
   (= (path-length C-DS OUTPUT C-BS INPUT) 6.578718)
   (= (path-length C-DS OUTPUT C-BS OUTPUT) 6.093977)
   (= (path-length C-DS OUTPUT C-CS1 INPUT) 10.289251)
   (= (path-length C-DS OUTPUT C-CS1 OUTPUT) 8.201967)
   (= (path-length C-DS OUTPUT C-CS2 INPUT) 6.489504)
   (= (path-length C-DS OUTPUT C-CS2 OUTPUT) 6.240150)
   (= (path-length C-DS OUTPUT C-DS INPUT) 3.342638)
   (= (path-length START INPUT C-BS INPUT) 0.930239)
   (= (path-length START INPUT C-BS OUTPUT) 3.141956)
   (= (path-length START INPUT C-CS1 INPUT) 10.444141)
   (= (path-length START INPUT C-CS1 OUTPUT) 10.994568)
   (= (path-length START INPUT C-CS2 INPUT) 3.531090)
   (= (path-length START INPUT C-CS2 OUTPUT) 2.405819)
   (= (path-length START INPUT C-DS INPUT) 7.510794)
   (= (path-length START INPUT C-DS OUTPUT) 6.404583))

  (:goal (order-fulfilled o1))
)
