echo -e "===============================================================================\n"
echo -e "Start Planning Testing\n"
echo -e "===============================================================================\n"
echo -e "\n"
echo -e "===============================================================================\n"
echo -e "Situated Temporal Planning\n"
echo -e "===============================================================================\n"
./rewrite-no-lp --time-based-on-expansions-per-second 500 --expansion-limit 100000 --include-metareasoning-time --real-to-plan-time-multiplier 1 --calculate-Q-interval 100  --min-probability-failure 0.001  --slack-from-heuristic  --forbid-self-overlapping-actions --deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 --icaps-for-n-expansions 100 --add-weighted-f-value-to-Q -0.000001 --time-aware-heuristic 1 --use-dispatcher LPFThreshold --dispatch-frontier-size 10 --subtree-focus-threshold 0.0125 --dispatch-threshold 0.025 --optimistic-lst-for-dispatch-reasoning driverlogTimed.pddl $1
echo -e "\n"
echo -e "===============================================================================\n"
echo -e "Offline Planning\n"
echo -e "===============================================================================\n"
./rewrite-no-lp  --expansion-limit 100000  --real-to-plan-time-multiplier 0  driverlogTimed.pddl $1
echo -e "\n"
echo -e "===============================================================================\n"
echo -e "Situated Planning\n"
echo -e "===============================================================================\n"
./rewrite-no-lp --time-based-on-expansions-per-second 500 --expansion-limit 100000 --include-metareasoning-time --real-to-plan-time-multiplier 1 --calculate-Q-interval 100  --min-probability-failure 0.001  --slack-from-heuristic  --forbid-self-overlapping-actions --deadline-aware-open-list IJCAI --ijcai-gamma 1 --ijcai-t_u 100 --icaps-for-n-expansions 100 --add-weighted-f-value-to-Q -0.000001 --time-aware-heuristic 1 driverlogTimed.pddl $1
echo -e "===============================================================================\n"
