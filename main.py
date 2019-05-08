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
	list_tuples = []
	f = open(name, 'r')
	for line in f:
		# # of flows, flow #, sample, completion time
		flow, n, s, time = line.split(":",4)
		time = float(time[:len(time)-2]) # rid of \n
		if flow == '93':
			t = (int(n),time)
			list_tuples.append(t)
	list_tuples.sort(key = lambda tup: tup[0])
	f_out = open('dist_data.txt', 'w')
	for t in list_tuples:
		f_out.write('{n0}:{n1}\n'.format(n0=t[0],n1=t[1]))
	f_out.close()

	f = open('dist_data.txt', 'r')
	data = np.array([])
	last_flow = 0
	avg_time = 0
	count = 0
	for line in f:
		flow,time = line.split(":",2)
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
	return np.sort(data)


def plot_line():
	plt.plot(line_data('design_3.txt'),label='TAALK')
	plt.plot(line_data('maglev_2.txt'),label='Maglev')
	plt.ylabel('Completion Time in seconds')
	plt.xlabel('Flow Number')
	plt.title("Completion Times for TAALK vs. Maglev")
	plt.legend(loc='upper left')
	plt.show()

def plot_dist(name):
	data = dist_data(name)
	plt.hist(data, normed=True, bins=10)
	plt.ylabel('Number of flows')
	plt.xlabel('Completion Time')
	if name == 'maglev_2.txt':
		s = 'Maglev'
	else:
		s = 'TAALK'
	plt.title("Frequency Histogram for " + s)
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
	plt.ylabel('Completion Time in Seconds')
	plt.xlabel('Flow Number')
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

	xmarks=[i for i in range(0,100,10)]
	plt.xticks(xmarks)
	plt.show()


# main
# plot_line()
# plot_box()
plot_dist('maglev_2.txt')
# plot_dist('design_3.txt')

