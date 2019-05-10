import matplotlib.pyplot as plt
import numpy as np
import math

BLUE='#3562e8'
RED='#f75959'
FONT_SIZE=30

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

def max_line_data(name):
	f = open(name, 'r')
	data = np.array([])
	last_flow = 0
	max_time = 0
	for line in f:
		flow, _, _, time = line.split(":",4)
		time = float(time[:len(time)-2]) # rid of \n
		if last_flow != flow:
			if last_flow != 0:
				data = np.append(data,max_time)
			# set up next
			last_flow = flow
			max_time = time
		else:
			if max_time < time:
				max_time = time
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

def all_dist_data(name):
	f = open(name, 'r')
	data = []
	for line in f:
		# # of flows, flow #, sample, completion time
		flow, n, s, time = line.split(":",4)
		time = float(time[:len(time)-2]) # rid of \n
		if flow == '93':
			data.append(time)
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

def plot_avg_line():
	plt.plot(line_data('maglev_2.txt'),label='Maglev',color=RED,linewidth=7)
	plt.plot(line_data('design_3.txt'),label='TAALK',color=BLUE,linewidth=7)
	plt.ylabel('Completion Time in seconds')
	plt.xlabel('Load')
	plt.title("Average Completion Times for TAALK vs. Maglev")
	plt.rcParams.update({'font.size': FONT_SIZE})

	leg = plt.legend(loc='upper left')
	# get the lines and texts inside legend box
	leg_lines = leg.get_lines()
	leg_texts = leg.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leg_lines, linewidth=7)

	plt.show()

def plot_max_line():
	plt.plot(max_line_data('maglev_2.txt'),label='Maglev',color=RED,linewidth=7)
	plt.plot(max_line_data('design_3.txt'),label='TAALK',color=BLUE,linewidth=7)
	plt.ylabel('Completion Time in seconds')
	plt.xlabel('Load')
	plt.title("Job Completion Times for TAALK vs. Maglev")
	plt.rcParams.update({'font.size': FONT_SIZE})

	leg = plt.legend(loc='upper left')
	# get the lines and texts inside legend box
	leg_lines = leg.get_lines()
	leg_texts = leg.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leg_lines, linewidth=7)

	plt.show()

def plot_dist():
	maglev_data = all_dist_data('maglev_2.txt')
	design_data = all_dist_data('design_3.txt')
	binwidth = 0.1
	plt.hist(maglev_data, bins=np.arange(min(maglev_data), max(maglev_data) + binwidth, binwidth),color=RED,label='Maglev',alpha=0.5)
	plt.hist(design_data, bins=np.arange(min(maglev_data), max(maglev_data) + binwidth, binwidth),color=BLUE,label='TAALK',alpha=0.5)
	plt.ylabel('Number of flows')
	plt.xlabel('Completion Time in Seconds')
	plt.title('Frequency Histogram')
	plt.rcParams.update({'font.size': FONT_SIZE})

	leg = plt.legend(loc='upper right')
	# get the lines and texts inside legend box
	leg_lines = leg.get_lines()
	leg_texts = leg.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leg_lines, linewidth=7)

	plt.show()

def color_box(bp, color):
    # Define the elements to color. You can also add medians, fliers and means
    elements = ['boxes','caps','whiskers','medians','fliers']
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
	plt.xlabel('Load')
	plt.rcParams.update({'font.size': FONT_SIZE})
	# temp lines for legend
	plt.plot([], c=RED, label='Maglev')
	plt.plot([], c=BLUE, label='TAALK')
	design_data = box_data('design_3.txt')
	maglev_data = box_data('maglev_2.txt')

	bp_design = ax.boxplot(design_data)
	color_box(bp_design, BLUE)

	bp_maglev = ax.boxplot(maglev_data)
	color_box(bp_maglev, RED)

	xmarks=[i for i in range(0,100,10)]
	plt.xticks(xmarks)

	leg = plt.legend(loc='upper left')
	# get the lines and texts inside legend box
	leg_lines = leg.get_lines()
	leg_texts = leg.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leg_lines, linewidth=7)

	plt.show()


# main
# plot_avg_line()
# plot_max_line()
# plot_box()
plot_dist()

