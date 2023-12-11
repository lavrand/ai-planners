import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Raw data
data1 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 3, 14, 29, 51, 70, 83],
    'disp(0.025)': [3, 10, 32, 58, 75, 65, 79, 91],
    'disp(0.1)': [3, 14, 31, 60, 73, 70, 82, 89],
    'disp(0.25)': [3, 15, 30, 59, 68, 68, 82, 87]
}

data2 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 1, 4, 12, 23, 39, 56],
    'disp(0.025)': [4, 10, 21, 27, 26, 28, 28, 40],
    'disp(0.1)': [4, 10, 24, 27, 24, 26, 32, 41],
    'disp(0.25)': [3, 11, 24, 27, 24, 26, 29, 42]
}

data3 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [0, 0, 0, 0, 0, 5, 8, 9],
    'disp(0.025)': [0, 5, 8, 13, 25, 28, 27, 20],
    'disp(0.1)': [0, 4, 8, 8, 18, 23, 30, 33],
    'disp(0.25)': [1, 3, 7, 11, 20, 25, 22, 34]
}

data4 = {
    'EPS': [10, 25, 50, 100, 200, 300, 500, 1000],
    'nodisp': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.025)': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.1)': [100, 100, 100, 100, 100, 100, 100, 100],
    'disp(0.25)': [100, 100, 100, 100, 100, 100, 100, 100],
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
    plt.ylim(99.5, 100.1)  # Set y-axis limit
    y_ticks = plt.yticks()[0]
    y_ticks_labels = [str(int(tick)) if tick < 100.1 else '' for tick in y_ticks]
    plt.gca().set_yticklabels(y_ticks_labels)

    plt.legend(fontsize=14, loc='lower right', ncol=2)

    plt.text(0.05, 0.95, name, transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=18, bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=0.5))

    plt.savefig(name + '.png', bbox_inches='tight')

create_and_save_plot(data1, 1)
create_and_save_plot(data2, 2)
create_and_save_plot(data3, 3)
create_and_save_plot_name(data4, "Turtlebot")
