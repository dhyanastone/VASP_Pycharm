#!/usr/bin/python
# coding:utf-8

"""这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。
可以给出任务ID, Directory, Description (relax, scf, band, hse scf, hse band, etc),
Status (Queue, Run, Finished (Converged, Non-converged) (红字标出), Start Time,
Finish Time, Time Elapsed, Tips (Energy, Band Gap, etc))."""

# import os


def tracking_user():
    """这个函数返回跟踪任务的用户名。"""
    f_user_name = raw_input('请输入用户名称： ')
    f_user_dir = raw_input('\n请输入任务所在文件夹（建议从根目录/开始）： ')
    return f_user_name, f_user_dir


print '\n这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。' \
      '可以给出任务ID, Directory, Description (relax, scf, band, hse scf, hse band, etc),' \
      'Status (Queue, Run, Finished (Converged, Non-converged) (红字标出), Start Time,' \
      'Finish Time, Time Elapsed, Tips (Energy, Band Gap, etc))\n.'

# 指定跟踪用户和任务目录
user_name, user_dir = tracking_user()
print '\n好的，我们来记录用户%s在目录%s及其子目录下任务的运行状态。\n' % (user_name, user_dir)

with open('%s/JobsLog' % user_dir, 'w') as job_log:
    job_log.write('Jobs of %s in directory %s' % (user_name, user_dir))
