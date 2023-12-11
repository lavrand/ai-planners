# Parsing the provided example to calculate the makespan

data = """
19.155: (bailout kenny dock-station) [193.850] ; (0)
213.006: (goto_waypoint kenny dock-station phdarea) [116.990] ; (63)
324.997: (ask_unload kenny) [5.000] ; (105)
329.998: (wait_unload kenny phdarea) [15.000] ; (110)
344.998: (goto_waypoint kenny phdarea coffee) [133.725] ; (7)
478.724: (goto_waypoint kenny coffee phdarea) [133.725] ; (61)
612.450: (goto_waypoint kenny phdarea printer-ent) [124.205] ; (87)
731.656: (ask_load kenny) [5.000] ; (104)
731.658: (ask_load kenny) [5.000] ; (104)
731.659: (ask_load kenny) [5.000] ; (104)
731.660: (ask_load kenny) [5.000] ; (104)
731.661: (ask_load kenny) [5.000] ; (104)
731.662: (ask_load kenny) [5.000] ; (104)
731.663: (ask_load kenny) [5.000] ; (104)
731.664: (ask_load kenny) [5.000] ; (104)
731.665: (ask_load kenny) [5.000] ; (104)
731.666: (ask_load kenny) [5.000] ; (104)
731.667: (ask_load kenny) [5.000] ; (104)
731.668: (ask_load kenny) [5.000] ; (104)
731.669: (ask_load kenny) [5.000] ; (104)
731.670: (ask_load kenny) [5.000] ; (104)
736.657: (wait_load kenny) [15.000] ; (106)
751.657: (goto_waypoint kenny printer-ent coffee) [18.205] ; (9)
764.863: (ask_unload kenny) [5.000] ; (105)
769.864: (wait_unload kenny coffee) [15.000] ; (107)
784.864: (goto_waypoint kenny coffee printer-ent) [18.205] ; (81)
798.070: (ask_load kenny) [5.000] ; (104)
803.071: (wait_load kenny) [15.000] ; (106)
818.071: (goto_waypoint kenny printer-ent meeting-room) [16.475] ; (59)
829.547: (ask_unload kenny) [5.000] ; (105)
834.548: (wait_unload kenny meeting-room) [15.000] ; (109)
849.548: (goto_waypoint kenny meeting-room dock-station) [52.605] ; (26)
902.154: (dock kenny dock-station) [30.000] ; (102)
"""

# Extracting time and duration for each action and calculating the sum
makespan_values = []

for line in data.split('\n'):
    if ':' in line:
        parts = line.split(':')
        time = float(parts[0])
        duration = float(parts[1].split('[')[1].split(']')[0])
        makespan_values.append(time + duration)

# Finding the maximum value
max_makespan = max(makespan_values, default=0)
print(max_makespan)