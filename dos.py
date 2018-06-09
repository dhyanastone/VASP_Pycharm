#!/usr/bin/python
# coding: utf-8

import time
import os

"""这个程序可以处理VASP输出文件DOSCAR。初版完成于2017年2月27日。
2017年3月7日更新，费米能级从scf目录中读，不从DOSCAR文件中读。"""

start_time = time.time()

dos_data = []

print '这个程序可以处理VASP输出文件DOSCAR。\n'

print '我将从本目录读取费米能级。\n'
os.system('grep fermi OUTCAR | tail -1')
E_fermi = float(raw_input('请输入费米能级：\n'))
option = int(raw_input('请问要将费米能级移到0吗？（1：要；0：不要）\n'))
if option == 1:
    print "好的，我们把费米能级移到0."
elif option == 0:
    print "费米能级未移动。"
else:
    print '错误的选择。拜拜。'
    exit()
shift = E_fermi * option

print '我们来处理DOSCAR文件。\n'
print '我将会把数据写入dos.dat文件中。\n'
# Open DOSCAR
# with statement can call close() method automatically
with open('DOSCAR', 'r') as doscar:
    # 跳过前5行
    for i in range(5):
        doscar.readline()
    # 第6行数据依次是能量上限，能量下限，NEDOS，费米能级，不详。
    line_6 = map(float, doscar.readline().split())
    NEDOS = int(line_6[2])
    with open('dos.dat', 'w') as dos:
        os.system('grep ISPIN OUTCAR')
        ISPIN = int(raw_input('请输入ISPIN：\n'))
        if ISPIN == 1:
            print "这是一个自旋非极化计算。\n"
            for i in range(NEDOS):
                eigen_val = map(float, doscar.readline().split())
                dos_data.append(eigen_val[0] - shift)
                dos_data.append(eigen_val[1])
            for j in range(NEDOS):
                dos.write('%-10.4f' % dos_data[j * 2])
                dos.write('%-10.4f' % dos_data[j * 2 + 1])
                dos.write('\n')
        elif ISPIN == 2:
            print "这是一个自旋极化计算。\n"
            for i in range(NEDOS):
                eigen_val = map(float, doscar.readline().split())
                dos_data.append(eigen_val[0] - shift)
                dos_data.append(eigen_val[1])
                dos_data.append(eigen_val[2])
            for j in range(NEDOS):
                dos.write('%-10.4f' % dos_data[j * 3])
                dos.write('%-10.4f' % dos_data[j * 3 + 1])
                dos.write('%-10.4f' % (0.0 - dos_data[j * 3 + 2]))
                dos.write('\n')
        else:
            print '错误的选择。拜拜。'
            exit()

print '数据处理完毕。ENJOY.'
print '耗时%d秒。' % (time.time() - start_time)
