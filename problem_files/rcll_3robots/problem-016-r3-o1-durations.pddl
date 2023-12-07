(define (problem rcll-production-016-durative)
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
   
  (:init (order-delivery-window-open o1) (at 150 (not (order-delivery-window-open o1))) (can-commit-for-ontime-delivery o1) (at 15 (not (can-commit-for-ontime-delivery o1)))
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
   (order-base-color o1 BASE_BLACK)
   (order-cap-color o1 CAP_BLACK)
   (order-gate o1 GATE-3)



   (= (path-length C-BS INPUT C-BS OUTPUT) 2.615478)
   (= (path-length C-BS INPUT C-CS1 INPUT) 12.254657)
   (= (path-length C-BS INPUT C-CS1 OUTPUT) 10.963749)
   (= (path-length C-BS INPUT C-CS2 INPUT) 2.684118)
   (= (path-length C-BS INPUT C-CS2 OUTPUT) 5.160885)
   (= (path-length C-BS INPUT C-DS INPUT) 8.382800)
   (= (path-length C-BS INPUT C-DS OUTPUT) 8.838386)
   (= (path-length C-BS OUTPUT C-BS INPUT) 2.615478)
   (= (path-length C-BS OUTPUT C-CS1 INPUT) 10.303489)
   (= (path-length C-BS OUTPUT C-CS1 OUTPUT) 9.012581)
   (= (path-length C-BS OUTPUT C-CS2 INPUT) 3.341104)
   (= (path-length C-BS OUTPUT C-CS2 OUTPUT) 3.600969)
   (= (path-length C-BS OUTPUT C-DS INPUT) 6.834111)
   (= (path-length C-BS OUTPUT C-DS OUTPUT) 6.887218)
   (= (path-length C-CS1 INPUT C-BS INPUT) 12.254655)
   (= (path-length C-CS1 INPUT C-BS OUTPUT) 10.303488)
   (= (path-length C-CS1 INPUT C-CS1 OUTPUT) 2.623855)
   (= (path-length C-CS1 INPUT C-CS2 INPUT) 11.551559)
   (= (path-length C-CS1 INPUT C-CS2 OUTPUT) 11.258648)
   (= (path-length C-CS1 INPUT C-DS INPUT) 8.987787)
   (= (path-length C-CS1 INPUT C-DS OUTPUT) 8.096366)
   (= (path-length C-CS1 OUTPUT C-BS INPUT) 10.963748)
   (= (path-length C-CS1 OUTPUT C-BS OUTPUT) 9.012580)
   (= (path-length C-CS1 OUTPUT C-CS1 INPUT) 2.623856)
   (= (path-length C-CS1 OUTPUT C-CS2 INPUT) 10.260652)
   (= (path-length C-CS1 OUTPUT C-CS2 OUTPUT) 9.967740)
   (= (path-length C-CS1 OUTPUT C-DS INPUT) 8.549374)
   (= (path-length C-CS1 OUTPUT C-DS OUTPUT) 6.805459)
   (= (path-length C-CS2 INPUT C-BS INPUT) 2.684117)
   (= (path-length C-CS2 INPUT C-BS OUTPUT) 3.341104)
   (= (path-length C-CS2 INPUT C-CS1 INPUT) 11.551559)
   (= (path-length C-CS2 INPUT C-CS1 OUTPUT) 10.260652)
   (= (path-length C-CS2 INPUT C-CS2 OUTPUT) 3.106586)
   (= (path-length C-CS2 INPUT C-DS INPUT) 5.936915)
   (= (path-length C-CS2 INPUT C-DS OUTPUT) 8.135288)
   (= (path-length C-CS2 OUTPUT C-BS INPUT) 5.160886)
   (= (path-length C-CS2 OUTPUT C-BS OUTPUT) 3.600969)
   (= (path-length C-CS2 OUTPUT C-CS1 INPUT) 11.258648)
   (= (path-length C-CS2 OUTPUT C-CS1 OUTPUT) 9.967740)
   (= (path-length C-CS2 OUTPUT C-CS2 INPUT) 3.106586)
   (= (path-length C-CS2 OUTPUT C-DS INPUT) 3.565598)
   (= (path-length C-CS2 OUTPUT C-DS OUTPUT) 6.728811)
   (= (path-length C-DS INPUT C-BS INPUT) 8.382801)
   (= (path-length C-DS INPUT C-BS OUTPUT) 6.834111)
   (= (path-length C-DS INPUT C-CS1 INPUT) 8.987786)
   (= (path-length C-DS INPUT C-CS1 OUTPUT) 8.549374)
   (= (path-length C-DS INPUT C-CS2 INPUT) 5.936916)
   (= (path-length C-DS INPUT C-CS2 OUTPUT) 3.565598)
   (= (path-length C-DS INPUT C-DS OUTPUT) 3.207366)
   (= (path-length C-DS OUTPUT C-BS INPUT) 8.838386)
   (= (path-length C-DS OUTPUT C-BS OUTPUT) 6.887218)
   (= (path-length C-DS OUTPUT C-CS1 INPUT) 8.096365)
   (= (path-length C-DS OUTPUT C-CS1 OUTPUT) 6.805459)
   (= (path-length C-DS OUTPUT C-CS2 INPUT) 8.135287)
   (= (path-length C-DS OUTPUT C-CS2 OUTPUT) 6.728811)
   (= (path-length C-DS OUTPUT C-DS INPUT) 3.207366)
   (= (path-length START INPUT C-BS INPUT) 2.309678)
   (= (path-length START INPUT C-BS OUTPUT) 1.631392)
   (= (path-length START INPUT C-CS1 INPUT) 10.001838)
   (= (path-length START INPUT C-CS1 OUTPUT) 8.710931)
   (= (path-length START INPUT C-CS2 INPUT) 4.343280)
   (= (path-length START INPUT C-CS2 OUTPUT) 4.050368)
   (= (path-length START INPUT C-DS INPUT) 7.283510)
   (= (path-length START INPUT C-DS OUTPUT) 6.585568))

  (:goal (order-fulfilled o1))
)
