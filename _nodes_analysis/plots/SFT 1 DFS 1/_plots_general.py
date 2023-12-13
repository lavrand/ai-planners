import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Raw data
# +
data1 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 2, 15, 39, 48, 64, 79],  # Updated values
    'disp(0.025)': [2, 7, 20, 40, 35, 47, 54, 68],  # Updated values
    'disp(0.1)': [4, 8, 20, 47, 43, 43, 55, 74],  # Updated values
    'disp(0.25)': [3, 7, 20, 53, 56, 54, 61, 77]  # Updated values
}
# +
data2 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 1, 2, 16, 11, 23, 45],  # Updated values
    'disp(0.025)': [1, 3, 10, 15, 10, 9, 7, 15],  # Updated values
    'disp(0.1)': [2, 2, 2, 10, 10, 11, 10, 15],  # Updated values
    'disp(0.25)': [2, 2, 2, 8, 14, 7, 7, 9]  # Updated values
}

# +
data3 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 0, 0, 3, 6, 3, 13],  # Updated values
    'disp(0.025)': [0, 2, 2, 4, 3, 3, 1, 2],  # Updated values
    'disp(0.1)': [0, 1, 1, 3, 3, 3, 3, 1],  # Updated values
    'disp(0.25)': [0, 1, 0, 2, 3, 1, 5, 0]  # Updated values
}

# +
data4 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.025)': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.1)': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.25)': [100, 100, 100, 100, 100, 100, 100, 100],
}
# +
data5 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [83, 67, 100, 100, 100, 100, 100, 100],  # Updated values
    'disp(0.025)': [17, 67, 67, 67, 100, 100, 100, 100],  # Updated values
    'disp(0.1)': [50, 67, 83, 83, 100, 100, 100, 100],  # Updated values
    'disp(0.25)': [67, 67, 83, 100, 100, 100, 100, 100]  # Updated values
}

def create_and_save_plot(data, numRobots):
# Plotting
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'cmr10'

    plt.plot(data['EPS'], data['nodisp'], marker='o', label='nodisp', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.025)'], marker='s', label='disp(0.025)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.1)'], marker='^', label='disp(0.1)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.25)'], marker='d', label='disp(0.25)', linewidth=2)

    # Adding labels and legend
    plt.xlabel('Expansions Per Second', fontsize=18)
    plt.ylabel('% Solved', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc='lower right', ncol=2)


    # Add text box
    ending = ' Robot)' if numRobots == 1 else ' Robots)'
    plt.text(0.05, 0.95, "RCLL (" + str(numRobots)+ending, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none',alpha=0.5))


    # Save the plot as an image file
    plt.savefig( str(numRobots)+'.png', bbox_inches='tight')

def create_and_save_plot_rcll(data, numRobots):
# Plotting
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'cmr10'

    plt.plot(data['EPS'], data['nodisp'], marker='o', label='nodisp', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.025)'], marker='s', label='disp(0.025)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.1)'], marker='^', label='disp(0.1)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.25)'], marker='d', label='disp(0.25)', linewidth=2)

    # Adding labels and legend
    plt.xlabel('Expansions Per Second', fontsize=18)
    plt.ylabel('% Solved', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc='lower right', ncol=2)


    # Add text box
    ending = ' Robot)' if numRobots == 1 else ' Robots)'
    plt.text(0.05, 0.95, "RCLL (" + str(numRobots)+ending, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none',alpha=0.5))


    # Save the plot as an image file
    plt.savefig("RCLL " + str(numRobots)+'.png', bbox_inches='tight')

def create_and_save_plot_name_100(data, name):
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'cmr10'

    # Introduce small variations if all values are 100%
    if all(v == 100 for v in data['nodisp']):
        data['nodisp'] = np.array(data['nodisp']) + 0.0
        data['disp(0.025)'] = np.array(data['disp(0.025)']) - 0.004
        data['disp(0.1)'] = np.array(data['disp(0.1)']) + 0.004
        data['disp(0.25)'] = np.array(data['disp(0.25)']) - 0.008

    plt.plot(data['EPS'], data['nodisp'], marker='o', label='nodisp', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.025)'], marker='s', label='disp(0.025)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.1)'], marker='^', label='disp(0.1)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.25)'], marker='d', label='disp(0.25)', linewidth=2)

    plt.xlabel('Expansions Per Second', fontsize=18)
    plt.ylabel('% Solved', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(99.5, 100.1)  # Set y-axis limit
    y_ticks = plt.yticks()[0]
    y_ticks_labels = [f"{tick:.1f}" if tick < 100.1 else '' for tick in y_ticks]
    plt.gca().set_yticklabels(y_ticks_labels)

    plt.legend(fontsize=14, loc='lower right', ncol=2)

    plt.text(0.05, 0.95, name, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=0.5))

    plt.savefig(name + '.png', bbox_inches='tight')

def create_and_save_plot_name_up_to_100(data, name):
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'cmr10'

    # Introduce small variations if all values are 100%
    if all(v == 100 for v in data['nodisp']):
        data['nodisp'] = np.array(data['nodisp']) + 0.0
        data['disp(0.025)'] = np.array(data['disp(0.025)']) - 0.4
        data['disp(0.1)'] = np.array(data['disp(0.1)']) + 0.4
        data['disp(0.25)'] = np.array(data['disp(0.25)']) - 0.8

    plt.plot(data['EPS'], data['nodisp'], marker='o', label='nodisp', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.025)'], marker='s', label='disp(0.025)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.1)'], marker='^', label='disp(0.1)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.25)'], marker='d', label='disp(0.25)', linewidth=2)

    plt.xlabel('Expansions Per Second', fontsize=18)
    plt.ylabel('% Solved', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(0, 120)  # Set y-axis limit
    y_ticks = plt.yticks()[0]
    y_ticks_labels = [f"{tick:.1f}" if tick < 100.1 else '' for tick in y_ticks]
    plt.gca().set_yticklabels(y_ticks_labels)

    plt.legend(fontsize=14, loc='lower right', ncol=2)

    plt.text(0.05, 0.95, name, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=0.5))

    plt.savefig(name + '.png', bbox_inches='tight')

def create_and_save_plot_name(data, name):
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'cmr10'

    # Introduce small variations if all values are 100%
    if all(v == 100 for v in data['nodisp']):
        data['nodisp'] = np.array(data['nodisp']) + 0.0
        data['disp(0.025)'] = np.array(data['disp(0.025)']) - 0.004
        data['disp(0.1)'] = np.array(data['disp(0.1)']) + 0.004
        data['disp(0.25)'] = np.array(data['disp(0.25)']) - 0.008

    plt.plot(data['EPS'], data['nodisp'], marker='o', label='nodisp', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.025)'], marker='s', label='disp(0.025)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.1)'], marker='^', label='disp(0.1)', linewidth=2)
    plt.plot(data['EPS'], data['disp(0.25)'], marker='d', label='disp(0.25)', linewidth=2)

    plt.xlabel('Expansions Per Second', fontsize=18)
    plt.ylabel('% Solved', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc='lower right', ncol=2)

    plt.text(0.05, 0.95, name, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=0.5))

    plt.savefig(name + '.png', bbox_inches='tight')

create_and_save_plot_rcll(data1, 1)
create_and_save_plot_rcll(data2, 2)
create_and_save_plot_rcll(data3, 3)
create_and_save_plot_name_100(data4, "Turtlebot 1")
create_and_save_plot_name_up_to_100(data5, "Turtlebot 2")
