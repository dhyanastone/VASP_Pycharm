#!/usr/bin/python
# coding:utf-8

"""Give Job ID, Status (P, R, F), Tips, Directory."""

import os


def job_status():
    """Write job status to Job_status"""
    # get job check command
    with open('JobsLog', 'r') as job_log:
        # skip two lines
        for i in range(2):
            job_log.readline()
        command = ' '.join(job_log.readline().split()[4:])
        os.system('%s > .Job_status' % command)


def job_dir(job_id):
    """Return job directory. Modify this function according to your system."""
    # get job information, write to file .qstat
    os.system("scontrol show job %s > .qstat" % job_id)
    with open('.qstat', 'r') as my_qstat:
        f_lines = my_qstat.readlines()
        for f_line in f_lines:
            if 'WorkDir' not in f_line:
                f_lines = f_lines[1:]
            else:
                break
        total = []
        for f_line in f_lines:
            total.append(f_line.lstrip().strip())
        # join list
        total = "+-+-".join(total)
        total = total[8:]
        # sperate with '+-+-'
        total = total.split('+-+-')
        job_directory = total[0]
        os.system('rm -f .qstat')
    return job_directory


def file_sort(file_name):
    """Sort file."""
    with open(file_name, 'r') as f_file:
        # save to a list
        my_file = f_file.readlines()
        # save first 6 lines as file_head
        file_head = my_file[:6]
        # delete first 6 lines
        my_file = my_file[6:]
        # sorting, change '55' accordingly
        my_file.sort(lambda x, y: cmp(x.strip()[55:], y.strip()[55:]))
        total_my_file = file_head + my_file
        with open(file_name, 'w') as Sorted_Joblogs:
            # write the sorted list to file
            Sorted_Joblogs.writelines(total_my_file)


def underline_qr(qr):
    with open(qr, 'r') as q_r:
        q_r_lines = q_r.readlines()
    with open(qr, 'w') as q_r:
        for q_r_line in q_r_lines:
            q_r.write(q_r_line)
            if q_r_line[20:24] == 'P   ':
                q_r.write('*****************************************************************************************\n')
            elif q_r_line[20:24] == 'R   ':
                q_r.write('-----------------------------------------------------------------------------------------\n')
            else:
                pass


def delete_qr(qr):
    with open(qr, 'r') as q_r:
        q_r_lines = q_r.readlines()
    with open(qr, 'w') as q_r:
        for q_r_line in q_r_lines:
            if q_r_line[0:4] == '****' or q_r_line[0:4] == '----':
                continue
            else:
                q_r.write(q_r_line)

def job_update():
    """According to file Job_status, modify JobLog."""
    with open('JobsLog', 'a+') as job_log:
        # skip first 6 lines
        for i in range(6):
            job_log.readline()
        for line in job_log.readlines():
            # get job ID
            my_job_id = line.split()[0]
            # get job status
            my_job_status = line.split()[1]
            if my_job_status == 'P' or my_job_status == 'R':
                os.system('grep %s .Job_status > .Tmp1' % my_job_id)
                with open('.Tmp1', 'r') as tmp:
                    if tmp.readline() == '':
                        print 'Job %s has finished. Update JobLog.\n' % my_job_id
                        # update
                        os.system("sed -i 's/%s /F /g' JobsLog" % my_job_status)
                    else:
                        pass
            else:
                pass

    with open('.Job_status', 'r') as jobs_status:
        # skip some lines, modify according to your system
        for i in range(1):
            jobs_status.readline()
        for line in jobs_status.readlines():
            line = line.lstrip()
            # get job ID
            my_job_id = line.split()[0]
            # get job status
            my_job_status = line.split()[4]
            my_job_status = my_job_status[0:1]
            # get job directory
            my_job_directory = job_dir(my_job_id)
            os.system('pwd > .pwd')
            with open('.pwd', 'r') as pwd:
                # delete '\n' at the end
                working_dir = pwd.readline().strip()  + '/'
                # whether should I track this job ?
                if working_dir in my_job_directory:
                    os.system('grep %s JobsLog > .Tmp2' % my_job_id)
                    with open('.Tmp2', 'r') as tmp:
                        if tmp.readline() != '':
                            print '%s is an old job.' % my_job_id
                            os.system('grep %s JobsLog | cut -c 20-21 > .P_R_F' % my_job_id)
                            with open('.P_R_F', 'r') as p_r_f:
                                line = p_r_f.readline().split()
                                if my_job_status == line[0]:
                                    print 'No need to update %s status.\n' % my_job_id
                                else:
                                    # delete old status
                                    with open('JobsLog', 'r') as r_job_log:
                                        lines = r_job_log.readlines()
                                    with open('JobsLog', 'w') as w_job_log:
                                        for line_1 in lines:
                                            if my_job_id in line_1:
                                                continue
                                            w_job_log.write(line_1)
                                    # write new status
                                    with open('JobsLog', 'a') as job_log:
                                        job_log.write('%-20s%-15s%-20s%s\n' % (my_job_id, my_job_status,
                                                                               '', my_job_directory))
                                    print 'Update %s\n' % my_job_id
                        else:
                            # new job
                            print '%s is a new job. Tracking...\n' % my_job_id
                            with open('JobsLog', 'a') as job_log:
                                job_log.write('%-20s%-15s%-20s%s\n' % (my_job_id, my_job_status,
                                                                       '', my_job_directory))
                else:
                    pass


print '\nThis script can track job ID, Status (P, R, F), Tips, Directory.\n'

job_status()
delete_qr('JobsLog')
job_update()
file_sort('JobsLog')
underline_qr('JobsLog')
# delete temp files
os.system('rm -f .Job_status .Tmp1 .Tmp2 .P_R_F .pwd')
# delete configure.py
os.system('rm -f configure_nersc.py')
