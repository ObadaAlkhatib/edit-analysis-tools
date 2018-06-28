from datetime import datetime
import datetime
from time import strftime
import time
from datetime import timedelta
import matplotlib.pylab as plt


def activity_monitor(projects):        # takes in a projects file,
                                       # and returns a multi-layer dictionary with data ready to be plotted
                                       # (clock marks vs number of edits per 2 minutes, which can be changed as we wish)
    graphs = {}
    for i in range(len(projects)):

        sessions = {}
        sessions['session 0'] = {}
        session_number, in_session_index, count = 0, 0, 0
        set_activity_period = 120    # seconds
        session_timeout = 120     # minutes


        activity_start_str = projects[i].snapshots[0].send_date.strftime("%H:%M")
        activity_start = projects[i].snapshots[0].send_date
        date = activity_start.strftime("%d %B, %Y")

        for snap in range(len(projects[i].snapshots)):      

            time_mark = (activity_start + datetime.timedelta(minutes = set_activity_period*(in_session_index)/60))
            current_time = projects[i].snapshots[snap].send_date


            if projects[i].snapshots[snap].send_date_delta.total_seconds()/60 >= session_timeout:   # if idle for more than 2 hours, then new session begins
                in_session_index, count = 0, 1
                session_number += 1
                sessions['session %s' %session_number] = {}
                activity_start = projects[i].snapshots[snap].send_date
                date = activity_start.strftime("%d %B, %Y")

            else:
                
                if (current_time - time_mark).total_seconds() <= set_activity_period:
                    count += 1
                    if snap < len(projects[i].snapshots) - 1:
                        if projects[i].snapshots[snap + 1].send_date_delta.total_seconds()/60 >= session_timeout:
                            sessions['session %s' %session_number][in_session_index] = (time_mark.strftime("%H:%M"), count, date, time_mark)

                elif (current_time - time_mark).total_seconds() > set_activity_period and (current_time - time_mark).total_seconds() <= 2*set_activity_period:
                    count += 1
                    sessions['session %s' %session_number][in_session_index] = (time_mark.strftime("%H:%M"), count, date, time_mark)
                    in_session_index += 1
                    count = 0

                else:
                    count += 1
                    sessions['session %s' %session_number][in_session_index] = (time_mark.strftime("%H:%M"), count, date, time_mark)
                    in_session_index += 1
                    count = 0

                    for j in range(int(((current_time - time_mark).total_seconds() - set_activity_period)//set_activity_period)):
                        time_mark = (activity_start + datetime.timedelta(minutes = set_activity_period*(in_session_index)/60))
                        sessions['session %s' %session_number][in_session_index] = (time_mark.strftime("%H:%M"), count, date, time_mark)
                        in_session_index += 1

        time_mark = (activity_start + datetime.timedelta(minutes = set_activity_period*(in_session_index)/60))
        sessions['session %s' %session_number][in_session_index] = (time_mark.strftime("%H:%M"), count, date, time_mark)

                # some of the points on the plots could be off by one edit

        num_sessions = len(sessions)
        X_real_time = [list() for n in range(num_sessions)]
        Y = [list() for n in range(num_sessions)]
        date = [None]*num_sessions
        time_marks = [list() for n in range(num_sessions)]
        num = 0

        for session in sessions:
            
            for active_time in sessions[session]:
                time_marks[num].append(sessions[session][active_time][3])
                date[num] = sessions[session][active_time][2]
                Y[num].append(sessions[session][active_time][1])
                X_real_time[num].append(sessions[session][active_time][0])
                
            num += 1

        graphs['project %s' %i] = (X_real_time, Y, date, time_marks)    

    return graphs



def graph_activity(graphs):             # sequentially plots one session at a time, starting with session 1 project 1 and ending with the last session in the final project

    project_number = 1

    for project in graphs:

        num_sessions = len(graphs[project][0])
        
        for session_number in range(num_sessions):

            plt.clf()
            plt.title(('Project %s ' %(project_number)) + ('Session Number %r' %(session_number + 1)) + ' - ' + graphs[project][2][session_number])
            plt.xlabel('Time marks')
            plt.ylabel('Number of edits per 2 minutes')
            plt.scatter(graphs[project][0][session_number], graphs[project][1][session_number])
            plt.plot(graphs[project][0][session_number], graphs[project][1][session_number])
            input('Press any key to display next plot')

            plt.show()

        project_number += 1