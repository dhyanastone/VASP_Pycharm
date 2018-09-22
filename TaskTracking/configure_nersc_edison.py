#!/usr/bin/python
# coding:utf-8

"""This program can deal with username, JobDir, job check command."""

import os


def tracking_user_dir():
    """Return username and JobDir."""
    f_user_name = raw_input('Input your username:\n')
    os.system('pwd > .pwd')
    f_user_dir = raw_input('Input job directory (default: current dir):\n')
    if f_user_dir == '':
        with open('.pwd', 'r') as pwd:
            f_user_dir = pwd.readline().strip()
    else:
        pass
    return f_user_name, f_user_dir


def linux_command():
    """Return job check command"""
    f_command = raw_input('Input job check command (default: squeue -u liuqh):\n')
    if f_command == '':
        f_command = 'squeue -u liuqh'
    else:
        pass
    return f_command


print 'Configuring...\n'

# get username and job dir
user_name, user_dir = tracking_user_dir()
print "\nOK. Let's track jobs of %s in %s and subdirectory.\n" % (user_name, user_dir)

# get job check command
command = linux_command()

with open('%s/JobsLog' % user_dir, 'w') as job_log:
    job_log.write('Jobs of %s in directory %s\n\n' % (user_name, user_dir))
    job_log.write("Check jobs' status command: %s\n\n" % command)
    job_log.write('%-20s%-15s%-20s%s\n' % ('job ID', 'Status', 'Tips', 'Directory'))
    job_log.write('=========================================================================================\n')
    print '\nFinished. Written in file JobLog.'

