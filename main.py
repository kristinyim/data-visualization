import matplotlib.pyplot as plt
import numpy as np
import math

def line_data(name):
	f = open(name, 'r')
	data = np.array([])
	last_flow = 0
	avg_time = 0
	count = 0
	for line in f:
		flow, _, _, time = line.split(":",4)
		time = float(time[:len(time)-2]) # rid of \n
		if last_flow != flow:
			if last_flow != 0:
				data = np.append(data,(avg_time/count))
			# set up next
			last_flow = flow
			avg_time = time
			count = 1
		else:
			avg_time += time
			count += 1
	return data

def box_data(name):
	f = open(name, 'r')
	last_flow = 0
	data = []
	for line in f:
		flow, _, _, time = line.split(":",4)
		time = float(time[:len(time)-2]) # rid of \n
		if last_flow != flow:
			if last_flow != 0:
				data.append(flow_data)
				# data = np.append(data,(avg_time/count))
			# set up next
			last_flow = flow
			flow_data = np.append([],time)
		else:
			flow_data = np.append(flow_data,time)
	return data

def dist_data(name):
	f = open(name, 'r')
	last_flow = 0
	data = np.array([])
	for line in f:
		flow, _, _, time = line.split(":",4)
		if flow == '93':
			data = np.append(data,time)
	return np.sort(data)

def plot_line():
	plt.plot(line_data('design_3.txt'),label='TAALK')
	plt.plot(line_data('maglev_2.txt'),label='Maglev')
	plt.ylabel('Completion Time')
	plt.xlabel('Flow')
	plt.title("Completion Times for TAALK vs. Maglev")
	plt.legend(loc='upper left')
	plt.show()

def plot_dist():
	plt.plot(dist_data('design_3.txt'),label='TAALK')
	plt.plot(dist_data('maglev_2.txt'),label='Maglev')
	plt.ylabel('Completion Time')
	plt.xlabel('Sample')
	plt.title("Completion Times for Flow 93 for TAALK vs. Maglev")
	plt.legend(loc='upper left')
	# plt.ylim(top=2)
	plt.show()

def color_box(bp, color):

    # Define the elements to color. You can also add medians, fliers and means
    elements = ['boxes','caps','whiskers']

    # Iterate over each of the elements changing the color
    for elem in elements:
        [plt.setp(bp[elem][idx], color=color) for idx in xrange(len(bp[elem]))]
    return

def plot_box():
	fig, ax = plt.subplots()
	fig.set_figwidth(40)
	ax.set_title('Completion Times with Variance for TAALK vs. Maglev')
	ax.set_ylim(top=5)
	plt.xticks(rotation=90)
	plt.ylabel('Completion Time')
	plt.xlabel('Flow')
	# temp lines for legend
	plt.plot([], c='red', label='TAALK')
	plt.plot([], c='blue', label='Maglev')
	plt.legend(loc='upper left')
	design_data = box_data('design_3.txt')
	maglev_data = box_data('maglev_2.txt')
	bp_design = ax.boxplot(design_data)
	color_box(bp_design, 'red')
	bp_maglev = ax.boxplot(maglev_data)
	color_box(bp_maglev, 'blue')
	plt.show()


# main
# plot_box()
# plot_line()
plot_dist()

