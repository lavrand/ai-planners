(define (problem rcll-production-022-durative)
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



   (= (path-length C-BS INPUT C-BS OUTPUT) 2.798564)
   (= (path-length C-BS INPUT C-CS1 INPUT) 11.225394)
   (= (path-length C-BS INPUT C-CS1 OUTPUT) 12.572024)
   (= (path-length C-BS INPUT C-CS2 INPUT) 5.168159)
   (= (path-length C-BS INPUT C-CS2 OUTPUT) 6.573525)
   (= (path-length C-BS INPUT C-DS INPUT) 7.233031)
   (= (path-length C-BS INPUT C-DS OUTPUT) 6.943876)
   (= (path-length C-BS OUTPUT C-BS INPUT) 2.798564)
   (= (path-length C-BS OUTPUT C-CS1 INPUT) 11.146421)
   (= (path-length C-BS OUTPUT C-CS1 OUTPUT) 11.416960)
   (= (path-length C-BS OUTPUT C-CS2 INPUT) 3.812854)
   (= (path-length C-BS OUTPUT C-CS2 OUTPUT) 6.494553)
   (= (path-length C-BS OUTPUT C-DS INPUT) 5.877726)
   (= (path-length C-BS OUTPUT C-DS OUTPUT) 5.588571)
   (= (path-length C-CS1 INPUT C-BS INPUT) 11.225395)
   (= (path-length C-CS1 INPUT C-BS OUTPUT) 11.146421)
   (= (path-length C-CS1 INPUT C-CS1 OUTPUT) 3.056983)
   (= (path-length C-CS1 INPUT C-CS2 INPUT) 8.639973)
   (= (path-length C-CS1 INPUT C-CS2 OUTPUT) 6.822195)
   (= (path-length C-CS1 INPUT C-DS INPUT) 8.916682)
   (= (path-length C-CS1 INPUT C-DS OUTPUT) 7.479318)
   (= (path-length C-CS1 OUTPUT C-BS INPUT) 12.572025)
   (= (path-length C-CS1 OUTPUT C-BS OUTPUT) 11.416960)
   (= (path-length C-CS1 OUTPUT C-CS1 INPUT) 3.056983)
   (= (path-length C-CS1 OUTPUT C-CS2 INPUT) 9.986603)
   (= (path-length C-CS1 OUTPUT C-CS2 OUTPUT) 7.362899)
   (= (path-length C-CS1 OUTPUT C-DS INPUT) 8.495463)
   (= (path-length C-CS1 OUTPUT C-DS OUTPUT) 7.058098)
   (= (path-length C-CS2 INPUT C-BS INPUT) 5.168159)
   (= (path-length C-CS2 INPUT C-BS OUTPUT) 3.812853)
   (= (path-length C-CS2 INPUT C-CS1 INPUT) 8.639972)
   (= (path-length C-CS2 INPUT C-CS1 OUTPUT) 9.986603)
   (= (path-length C-CS2 INPUT C-CS2 OUTPUT) 3.988104)
   (= (path-length C-CS2 INPUT C-DS INPUT) 4.984528)
   (= (path-length C-CS2 INPUT C-DS OUTPUT) 4.695373)
   (= (path-length C-CS2 OUTPUT C-BS INPUT) 6.573526)
   (= (path-length C-CS2 OUTPUT C-BS OUTPUT) 6.494553)
   (= (path-length C-CS2 OUTPUT C-CS1 INPUT) 6.822194)
   (= (path-length C-CS2 OUTPUT C-CS1 OUTPUT) 7.362898)
   (= (path-length C-CS2 OUTPUT C-CS2 INPUT) 3.988105)
   (= (path-length C-CS2 OUTPUT C-DS INPUT) 4.739697)
   (= (path-length C-CS2 OUTPUT C-DS OUTPUT) 2.961917)
   (= (path-length C-DS INPUT C-BS INPUT) 7.233031)
   (= (path-length C-DS INPUT C-BS OUTPUT) 5.877726)
   (= (path-length C-DS INPUT C-CS1 INPUT) 8.916681)
   (= (path-length C-DS INPUT C-CS1 OUTPUT) 8.495461)
   (= (path-length C-DS INPUT C-CS2 INPUT) 4.984528)
   (= (path-length C-DS INPUT C-CS2 OUTPUT) 4.739697)
   (= (path-length C-DS INPUT C-DS OUTPUT) 4.434896)
   (= (path-length C-DS OUTPUT C-BS INPUT) 6.943876)
   (= (path-length C-DS OUTPUT C-BS OUTPUT) 5.588571)
   (= (path-length C-DS OUTPUT C-CS1 INPUT) 7.479318)
   (= (path-length C-DS OUTPUT C-CS1 OUTPUT) 7.058097)
   (= (path-length C-DS OUTPUT C-CS2 INPUT) 4.695373)
   (= (path-length C-DS OUTPUT C-CS2 OUTPUT) 2.961917)
   (= (path-length C-DS OUTPUT C-DS INPUT) 4.434896)
   (= (path-length START INPUT C-BS INPUT) 1.980485)
   (= (path-length START INPUT C-BS OUTPUT) 1.901513)
   (= (path-length START INPUT C-CS1 INPUT) 9.318376)
   (= (path-length START INPUT C-CS1 OUTPUT) 10.665007)
   (= (path-length START INPUT C-CS2 INPUT) 3.602026)
   (= (path-length START INPUT C-CS2 OUTPUT) 4.666507)
   (= (path-length START INPUT C-DS INPUT) 6.043867)
   (= (path-length START INPUT C-DS OUTPUT) 5.754712))

  (:goal (order-fulfilled o1))
)
