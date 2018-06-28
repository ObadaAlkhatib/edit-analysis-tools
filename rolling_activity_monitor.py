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

		
		for snap in range(len(projects[i].snapshots)):

			activity_start = projects[i].snapshots[snap].send_date
			date = activity_start.strftime("%d %B, %Y")

			if projects[i].snapshots[snap].send_date_delta.total_seconds()/60 >= session_timeout:

				in_session_index, count = 0, 0
				session_number += 1
				sessions["session %s" %session_number] = {}
				sessions["session %s" %session_number][in_session_index] = (activity_start.strftime("%H:%M"), count, activity_start, date)

			else:

				for prev_snap in range(snap, -1, -1):
					if (activity_start - projects[i].snapshots[prev_snap].send_date).total_seconds() <= set_interval_length:
						count += 1
					else:
						break

				sessions["session %s" %session_number][in_session_index] = (activity_start.strftime("%H:%M"), count, activity_start, date)
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
