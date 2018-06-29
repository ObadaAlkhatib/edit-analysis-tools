from datetime import datetime
import datetime
from time import strftime
import time
from datetime import timedelta
import matplotlib.pylab as plt


def rolling_activity_monitor(projects):     # returns a value that works with graph_activity function from the other module
	
	data = {}
	for i in range(len(projects)):

		sessions = {}
		sessions['session 0'] = {}
		session_number, in_session_index, count = 0, 0, 0
		set_interval_length = 120    # seconds
		session_timeout = 120    # minutes
		point = 0
		snap_session_start = 0
		
		for snap in range(len(projects[i].snapshots)):

			activity_start = projects[i].snapshots[snap].send_date
			point = (activity_start - projects[i].snapshots[snap_session_start].send_date).total_seconds()
			date = activity_start.strftime("%d %B, %Y")

			if projects[i].snapshots[snap].send_date_delta.total_seconds()/60 >= session_timeout:

				snap_session_start = snap
				in_session_index, count, point = 0, 0, 0
				session_number += 1
				sessions["session %s" %session_number] = {}
				sessions["session %s" %session_number][in_session_index] = (point, count, activity_start, date)


			else:

				for prev_snap in range(snap, -1, -1):
					if (activity_start - projects[i].snapshots[prev_snap].send_date).total_seconds() <= set_interval_length:
						count += 1
					else:
						break

				sessions["session %s" %session_number][in_session_index] = (point, count, activity_start, date)
				count = 0
				in_session_index += 1


		num_sessions = len(sessions)
		X = [list() for n in range(num_sessions)]
		Y = [list() for n in range(num_sessions)]
		full_time_marks = [list() for n in range(num_sessions)]
		dates = [None]*num_sessions

		index = 0

		for session in sessions:
			for time_mark in sessions[session]:
				X[index].append(sessions[session][time_mark][0])
				Y[index].append(sessions[session][time_mark][1])
				full_time_marks[index].append(sessions[session][time_mark][2])
				dates[index] = sessions[session][time_mark][3]

			index += 1

		data["project %s" %i] = (X, Y, dates, full_time_marks)

	return data


def graph_activity_rolling(data):             # sequentially plots one session at a time, starting with session 1 project 1 and ending with the last session in the final project

    project_number = 1

    for project in data:

        num_sessions = len(data[project][0])
        
        for session_number in range(num_sessions):

            plt.clf()
            plt.title(('Project %s ' %(project_number)) + ('Session Number %r' %(session_number + 1)) + ' - ' + data[project][2][session_number])
            plt.xlabel('Time marks from start of session (seconds)')
            plt.ylabel('Number of edits in previous 2 minutes')
            plt.scatter(data[project][0][session_number], data[project][1][session_number])
            plt.plot(data[project][0][session_number], data[project][1][session_number])
            input('Press any key to display next plot')

            plt.show()

        project_number += 1



def high_activity_periods(data, activity_threshold = 30):      		   # This is just an arbitrary number for the threshold.

	active_periods = {}

	for project in data:

		active_periods[project] = {}

		for session_num in range(len(data[project][1])):

			active_periods[project]['session %s' %session_num] = []

			for point in range(len(data[project][1][session_num])):

				if data[project][1][session_num][point] >= activity_threshold:

					active_periods[project]['session %s' %session_num].append((data[project][3][session_num][point], data[project][1][session_num][point]))

	return active_periods
