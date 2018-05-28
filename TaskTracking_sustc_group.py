#!/usr/bin/python
# coding:utf-8

"""这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。
可以给出任务ID, Status (P, R, F), Tips, Directory."""

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


def job_dir(job_id):
    """此函数返回任务所在目录，需根据不同服务器修改。"""
    # 服务器变量$HOME
    my_home = '/home/liuqh'
    # 根据任务号获取任务信息，并写入文件.qstat
    os.system("bjobs -l %s > .qstat" % job_id)
    with open('.qstat', 'r') as my_qstat:
        f_lines = my_qstat.readlines()
        for f_line in f_lines:
            if 'Submitted' not in f_line:
                f_lines = f_lines[1:]
            else:
                break
        total = []
        for f_line in f_lines:
            total.append(f_line.lstrip().strip())
        # 合并列表中所有字符串
        total = "".join(total)
        # 以'CWD <$HOME'分割字符串
        total = total.split('CWD <$HOME')
        # 以'>,'分割字符串
        total = total[1].split('>,')
        job_directory = total[0]
        job_directory = my_home + job_directory
        os.system('rm -f .qstat')
    return job_directory


def file_sort(file_name):
    """这个程序可以对文件按行排列."""
    with open(file_name, 'r') as f_file:
        # 将文件存入列表
        my_file = f_file.readlines()
        # 前6行存入file_head
        file_head = my_file[:6]
        # 去掉前6行
        my_file = my_file[6:]
        # 排序，需要根据具体情况修改‘55’
        my_file.sort(lambda x, y: cmp(x.strip()[55:], y.strip()[55:]))
        total_my_file = file_head + my_file
        with open(file_name, 'w') as Sorted_Joblogs:
            # 将已排序的内容写入文件
            Sorted_Joblogs.writelines(total_my_file)


def underline_qr(qr):
    with open(qr, 'r') as q_r:
        q_r_lines = q_r.readlines()
    with open(qr, 'w') as q_r:
        for q_r_line in q_r_lines:
            q_r.write(q_r_line)
            if q_r_line[20:24] == 'Q   ':
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
            if my_job_status == 'P' or my_job_status == 'R':
                os.system('grep %s .Job_status > .Tmp1' % my_job_id)
                with open('.Tmp1', 'r') as tmp:
                    if tmp.readline() == '':
                        print '任务%s已完成，让我来更新JobsLog文件。\n' % my_job_id
                        # 更新记录
                        os.system("sed -i 's/%s /F /g' JobsLog" % my_job_status)
                    else:
                        pass
            else:
                pass

    with open('.Job_status', 'r') as jobs_status:
        # 跳过前几行，根据不同服务器修改
        for i in range(1):
            jobs_status.readline()
        for line in jobs_status.readlines():
            # 获得任务号
            for i in line:
                if i.isspace():
                    break
                else:
                    my_job_id = line.split()[0]
                    # 获得任务状态
                    my_job_status = line.split()[2]
                    my_job_status = my_job_status[0:1]
                    # 获得任务路径
                    my_job_directory = job_dir(my_job_id)
                    os.system('pwd > .pwd')
                    with open('.pwd', 'r') as pwd:
                        #  注意去掉末尾的\n
                        working_dir = pwd.readline().strip()
                    # 判断预记录任务目录是否在指定目录中
                    if working_dir in my_job_directory:
                        os.system('grep %s JobsLog > .Tmp2' % my_job_id)
                        with open('.Tmp2', 'r') as tmp:
                            if tmp.readline() != '':
                                print '%s是旧任务，我来看看是否需要更新。' % my_job_id
                                os.system('grep %s JobsLog | cut -c 20-21 > .P_R_F' % my_job_id)
                                with open('.P_R_F', 'r') as p_r_f:
                                    line = p_r_f.readline().split()
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
                                            job_log.write('%-20s%-15s%-20s%s\n' % (my_job_id, my_job_status,
                                                                                   '', my_job_directory))
                                        print '%s已更新。\n' % my_job_id
                            else:
                                # 任务刚提交
                                print '%s是新任务，让我来记录它。\n' % my_job_id
                                with open('JobsLog', 'a') as job_log:
                                    job_log.write('%-20s%-15s%-20s%s\n' % (my_job_id, my_job_status,
                                                                           '', my_job_directory))
                    else:
                        pass
                    break


print '\n这个程序可以跟踪服务器中指定目录（针对一个帐号多用户）VASP任务的状态。' \
      '可以给出任务ID, Status (P, R, F), Tips, Directory.\n'

job_status()
delete_qr('JobsLog')
job_update()
file_sort('JobsLog')
underline_qr('JobsLog')
# 删除临时文件，参数-f表示在文件不存在时不提示
os.system('rm -f .Job_status .Tmp1 .Tmp2 .P_R_F .pwd')
# 删除配置文件configure.py
os.system('rm -f configure_sustc_group.py')
