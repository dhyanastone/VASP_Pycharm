#!/usr/bin/python
# coding:utf-8

"""这个程序用来配置相关参数，如用户名，任务目录，查看任务命令"""

import os


def tracking_user_dir():
    """这个函数返回跟踪任务的用户名。"""
    f_user_name = raw_input('请输入用户名称： \n')
    os.system('pwd > .pwd')
    f_user_dir = raw_input('请输入任务所在文件夹绝对路径(default：当前目录)： \n')
    if f_user_dir == '':
        with open('.pwd', 'r') as pwd:
            f_user_dir = pwd.readline().strip()
    else:
        pass
    return f_user_name, f_user_dir


def linux_command():
    """这个函数返回查看任务运行状态的命令。"""
    f_command = raw_input('请输入查看任务运行状态的命令(default: qstat)： \n')
    if f_command == '':
        f_command = 'qstat'
    else:
        pass
    return f_command


print '我们先来配置一下相关参数。\n'

# 指定跟踪用户和任务目录
user_name, user_dir = tracking_user_dir()
print '\n好的，我们来记录用户%s在目录%s及其子目录下任务的运行状态。\n' % (user_name, user_dir)

# 指定查看任务运行状态命令
command = linux_command()

with open('%s/JobsLog' % user_dir, 'w') as job_log:
    job_log.write('Jobs of %s in directory %s\n\n' % (user_name, user_dir))
    job_log.write("Check jobs' status command: %s\n\n" % command)
    job_log.write('%-20s%-15s%-20s%s\n' % ('job ID', 'Status', 'Tips', 'Directory'))
    job_log.write('=========================================================================================\n')
    print '\n配置完成，已写入%s/JobsLog文件中。' % user_dir

