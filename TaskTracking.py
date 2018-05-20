#!/usr/bin/python
# coding:utf-8

"""这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。
可以给出任务ID, Status (Queue, Run, Finished (Converged, Non-converged) (红字标出),
Time Used, Directory."""

import os


def job_status():
    """此函数将任务状态写入文件Job_status"""
    # 读取配置好的查看任务命令
    with open('JobsLog', 'r') as job_log:
        # 跳过前两行
        for i in range(2):
            job_log.readline()
        command = job_log.readline().split()[4]
        os.system('%s > .Job_status' % command)


def job_update():
    """根据Job_status文件，对JobsLog进行修改。需要针对不同的服务器进行修改。"""
    with open('JobsLog', 'a+') as job_log:
        # 跳过前6行
        for i in range(6):
            job_log.readline()
        for line in job_log.readlines():
            # 获得任务号
            my_job_id = line.split()[0]
            # 获得任务状态
            my_job_status = line.split()[1]
            if my_job_status == 'Q' or my_job_status == 'R':
                os.system('grep %s .Job_status > .Tmp1' % my_job_id)
                with open('.Tmp1', 'r') as tmp:
                    if tmp.readline() == '':
                        print '任务%s已完成，让我来更新JobsLog文件。\n' % my_job_id
                        # 更新记录
                        os.system("sed -i 's/%s/Finished/g' JobsLog" % my_job_status)
                    else:
                        pass
            else:
                pass

    with open('.Job_status', 'r') as jobs_status:
        # 跳过前两行
        jobs_status.readline()
        jobs_status.readline()
        for line in jobs_status.readlines():
            # 获得任务号
            my_job_id = line.split()[0]
            # 获得任务状态
            my_job_status = line.split()[4]
            # 获得任务路径，需根据不同服务器修改
            os.system("qstat -f %s | grep PWD | head -1 | cut -d '=' -f 2 > .Dir" % my_job_id)
            os.system('pwd > .pwd')
            with open('.pwd', 'r') as pwd:
                #  注意去掉末尾的\n
                working_dir = pwd.readline().strip()
                with open('.Dir', 'r') as job_dir:
                    my_job_directory = job_dir.readline()
                    # 判断预记录任务目录是否在指定目录中
                    if working_dir in my_job_directory:
                        # 去掉最后的逗号
                        my_job_directory = my_job_directory[:-2]
                        # with open('JobsLog', 'a') as job_log:
                        os.system('grep %s JobsLog > .Tmp2' % my_job_id)
                        with open('.Tmp2', 'r') as tmp:
                            if tmp.readline() != '':
                                print '%s是旧任务，我来看看是否需要更新。' % my_job_id
                                os.system('grep %s JobsLog | cut -c 15-16 > .Q_R_F' % my_job_id)
                                with open('.Q_R_F', 'r') as q_r_f:
                                    line = q_r_f.readline().split()
                                    if my_job_status == line[0]:
                                        print '%s无需更新。\n' % my_job_id
                                    else:
                                        # 删除旧记录
                                        with open('JobsLog', 'r') as r_job_log:
                                            lines = r_job_log.readlines()
                                        with open('JobsLog', 'w') as w_job_log:
                                            for line_1 in lines:
                                                if my_job_id in line_1:
                                                    continue
                                                w_job_log.write(line_1)
                                        # 写入新记录
                                        with open('JobsLog', 'a') as job_log:
                                            job_log.write('%-15s%-10s%-15s%s\n' % (my_job_id, my_job_status,
                                                                                   'Time Used', my_job_directory))
                                        print '%s已更新。\n' % my_job_id
                            else:
                                # 任务刚提交
                                print '%s是新任务，让我来记录它。\n' % my_job_id
                                with open('JobsLog', 'a') as job_log:
                                    job_log.write('%-15s%-10s%-15s%s\n' % (my_job_id, my_job_status,
                                                                           'Time Used', my_job_directory))
                    else:
                        pass


print '\n这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。' \
      '可以给出任务ID, Status (Q, R, Finished (Converged, Non-converged) (红字标出), Time Used,' \
      'Directory).\n'

job_status()
job_update()
# 删除临时文件，参数-f表示在文件不存在时不提示
os.system('rm -f .Job_status .Tmp1 .Dir .Tmp2 .Q_R_F .pwd')
# 将配置文件configure隐藏
os.system('mv configure.py .configure.py')
