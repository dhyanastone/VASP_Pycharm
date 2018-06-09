#!/usr/bin/python
# coding: utf-8

import time
import os

"""这个程序可以处理VASP能带计算的输出文件DOSCAR,将态密度的数据按原子，按轨道
分开。初版完成于2017年2月27日。"""


def atom_list(vasp):
    """这个函数返回原子种类的字符串型列表。"""
    with open(vasp, 'r') as def_structure:
        # 跳过前5行
        for def_i in range(5):
            def_structure.readline()
        # 第6行原子种类行，将各个原子名称存入字符串型列表
        atom_name = def_structure.readline().split()
    return atom_name


def atom_num_list(vasp):
    """这个函数返回各个种类原子数目的整数型列表。"""
    with open(vasp, 'r') as def_structure:
        # 跳过前6行
        for def_i in range(6):
            def_structure.readline()
        # 第7行原子数目行，将各个种类原子数目存入整数型列表
        atom_num = map(int, def_structure.readline().split())
    return atom_num


def lm_phase(vasp):
    """这个函数根据DOSCAR数据结构，判断ISPIN值，LORBIT值及体系
    是否含f电子。"""
    with open(vasp, 'r') as def_input:
        # 跳过DOSCAR前5行
        for def_i in range(5):
            def_input.readline()
        # 第6行数据依次是能量上限，能量下限，NEDOS，费米能级，不详。
        def_line_6 = map(float, def_input.readline().split())
        def_nedos = int(def_line_6[2])
        # 跳过NEDOS+1行
        for def_i in range(def_nedos + 1):
            def_input.readline()
        my_length = len(def_input.readline().split())
        if my_length == 4:
            print '我猜测ISPIN=1，LORBIT=10，体系中不含f电子。'
            def_m_phases = ['s', 'p', 'd']
        elif my_length == 5:
            print '我猜测ISPIN=1，LORBIT=10，体系中含f电子。'
            def_m_phases = ['s', 'p', 'd', 'f']
        elif my_length == 7:
            print '我猜测ISPIN=2，LORBIT=10，体系中不含f电子。'
            def_m_phases = ['s_up', 's_down', 'p_up', 'p_down', 'd_up', 'd_down']
        elif my_length == 9:
            print '我猜测ISPIN=2，LORBIT=10，体系中含f电子。'
            def_m_phases = ['s_up', 's_down', 'p_up', 'p_down', 'd_up', 'd_down', 'f_up', 'f_down']
        elif my_length == 10:
            print '我猜测ISPIN=1，LORBIT=11，体系中不含f电子。'
            def_m_phases = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2']
        elif my_length == 17:
            print '我猜测ISPIN=1，LORBIT=11，体系中含f电子。'
            def_m_phases = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz',
                            'dx2', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']
        elif my_length == 19:
            print '我猜测ISPIN=2，LORBIT=11，体系中不含f电子。'
            def_m_phases = ['s_up', 's_down', 'py_up', 'py_down', 'pz_up', 'pz_down',
                            'px_up', 'px_down', 'dxy_up', 'dxy_down', 'dyz_up',
                            'dyz_down', 'dz2_up', 'dz2_down', 'dxz_up', 'dxz_down',
                            'dx2_up', 'dx2_down']
        elif my_length == 33:
            print '我猜测ISPIN=2，LORBIT=11，体系中含f电子。'
            def_m_phases = ['s_up', 's_down', 'py_up', 'py_down', 'pz_up', 'pz_down',
                            'px_up', 'px_down', 'dxy_up', 'dxy_down', 'dyz_up',
                            'dyz_down', 'dz2_up', 'dz2_down', 'dxz_up', 'dxz_down',
                            'dx2_up', 'dx2_down', 'f1_up', 'f1_down', 'f2_up', 'f2_down',
                            'f3_up', 'f3_down', 'f4_up', 'f4_down', 'f5_up', 'f5_down',
                            'f6_up', 'f6_down', 'f7_up', 'f7_down']
        else:
            print '我无法判断ISPIN值，LORBIT值及体系是否含f电子，请检查。'
            def_m_phases = []
    return def_m_phases


start_time = time.time()

atom_names = atom_list('POSCAR')
print '看起来你的体系中有这些原子%s。' % atom_names
print '我将为每种原子建立一个文件夹。'
for atom in atom_names:
    if os.path.exists(atom):
        os.system('rm ./%s/*' % atom)
    else:
        os.mkdir(atom)
atom_numbers = atom_num_list('POSCAR')
print '看起来对应原子的数目是%s。' % atom_numbers

eigen_val = []
dos_data = []

with open('DOSCAR', 'r') as doscar:
    # 跳过前5行
    for i in range(5):
        doscar.readline()
    # 第6行数据依次是能量上限，能量下限，NEDOS，费米能级，不详。
    line_6 = map(float, doscar.readline().split())
    NEDOS = int(line_6[2])
    E_fermi = line_6[3]
    option = int(raw_input('请问要将费米能级移到0吗？（1：要；0：不要）\n'))
    if option == 1:
        print "好的，我们把费米能级移到0."
    elif option == 0:
        print "费米能级未移动。"
    else:
        print '错误的选择。拜拜。'
        exit()
    shift = E_fermi * option

    # 将能量值存入eigen_val
    for j in range(NEDOS):
        energy = map(float, doscar.readline().split())
        eigen_val.append(energy[0] - shift)

    # 将所有态密度数据存入dos_data列表
    for atom_numbers_i in range(sum(atom_numbers)):
        doscar.readline()
        for NEDOS_j in range(NEDOS):
            dos_data.extend(doscar.readline().split()[1:])
dos_data = map(float, dos_data)

m_phases = lm_phase('DOSCAR')

# 检查LORBIT参数
os.system('grep LORBIT INCAR')
# 检查ISPIN参数
os.system('grep ISPIN INCAR')

# 下面这段程序将DOSCAR的数据按原子类别,自旋上下,l(轨道)分开
val = []
if (len(m_phases) == 3) or (len(m_phases) == 4) \
        or (len(m_phases) == 6) or (len(m_phases) == 8):
    for n in range(NEDOS):
        for m in range(len(m_phases)):
            for k, atom in enumerate(atom_names):
                val = [0] * len(m_phases)
                for l in range(atom_numbers[k]):
                    index = m + ((l + (sum(atom_numbers) - sum(atom_numbers[k:])))
                                 * NEDOS + n) * len(m_phases)
                    val[m] += dos_data[index]
                with open('./%s/%s_l' % (atom, atom), 'a+') as atom_file:
                    atom_file.write('%-10.4f' % val[m])
                    if m == len(m_phases) - 1:
                        atom_file.write('\n')
    for atom in atom_names:
        with open('./%s/%s_l' % (atom, atom), 'r') as file1:
            with open('./%s/%s_l.dat' % (atom, atom), 'w') as file2:
                for i in range(NEDOS):
                    file2.write('%-10.4f%s' % (eigen_val[i], file1.readline()))
    for atom in atom_names:
        os.system('rm ./%s/%s_l' % (atom, atom))
elif (len(m_phases) == 9) or (len(m_phases) == 16):
    for n in range(NEDOS):
        for m in range(len(m_phases)):
            for k, atom in enumerate(atom_names):
                val = [0] * len(m_phases)
                for l in range(atom_numbers[k]):
                    index = m + ((l + (sum(atom_numbers) - sum(atom_numbers[k:])))
                                 * NEDOS + n) * len(m_phases)
                    val[m] += dos_data[index]
                with open('./%s/%s_l' % (atom, atom), 'a+') as atom_file:
                    atom_file.write('%-10.4f' % val[m])
                    if m == len(m_phases) - 1:
                        atom_file.write('\n')
    for atom in atom_names:
        with open('./%s/%s_l' % (atom, atom), 'r') as file1:
            with open('./%s/%s_l.dat' % (atom, atom), 'w') as file2:
                if len(m_phases) == 9:
                    for i in range(NEDOS):
                        file1_data = map(float, file1.readline().split())
                        file2.write('%-10.4f%-10.4f%-10.4f%-10.4f\n'
                                    % (eigen_val[i], file1_data[0],
                                       (file1_data[1] + file1_data[2] + file1_data[3]),
                                       (file1_data[4] + file1_data[5] + file1_data[6] +
                                        file1_data[7] + file1_data[8])))
                else:
                    for i in range(NEDOS):
                        file1_data = map(float, file1.readline().split())
                        file2.write('%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f\n'
                                    % (eigen_val[i], file1_data[0],
                                       (file1_data[1] + file1_data[2] + file1_data[3]),
                                       (file1_data[4] + file1_data[5] + file1_data[6] +
                                        file1_data[7] + file1_data[8]),
                                       (file1_data[9] + file1_data[10] + file1_data[11] +
                                        file1_data[12] + file1_data[13] + file1_data[14] +
                                        file1_data[15])
                                       ))
    for atom in atom_names:
        os.system('rm ./%s/%s_l' % (atom, atom))
elif (len(m_phases) == 18) or (len(m_phases) == 32):
    for n in range(NEDOS):
        for m in range(len(m_phases)):
            for k, atom in enumerate(atom_names):
                val = [0] * len(m_phases)
                for l in range(atom_numbers[k]):
                    index = m + ((l + (sum(atom_numbers) - sum(atom_numbers[k:])))
                                 * NEDOS + n) * len(m_phases)
                    val[m] += dos_data[index]
                with open('./%s/%s_l' % (atom, atom), 'a+') as atom_file:
                    atom_file.write('%-10.4f' % val[m])
                    if m == len(m_phases) - 1:
                        atom_file.write('\n')
    for atom in atom_names:
        with open('./%s/%s_l' % (atom, atom), 'r') as file1:
            with open('./%s/%s_l.dat' % (atom, atom), 'w') as file2:
                if len(m_phases) == 18:
                    for i in range(NEDOS):
                        file1_data = map(float, file1.readline().split())
                        file2.write('%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f\n'
                                    % (eigen_val[i], file1_data[0], file1_data[1],
                                       (file1_data[2] + file1_data[4] + file1_data[6]),
                                       (file1_data[3] + file1_data[5] + file1_data[7]),
                                       (file1_data[8] + file1_data[10] + file1_data[12] +
                                        file1_data[14] + file1_data[16]),
                                       (file1_data[9] + file1_data[11] + file1_data[13] +
                                        file1_data[15] + file1_data[17])))
                else:
                    for i in range(NEDOS):
                        file1_data = map(float, file1.readline().split())
                        file2.write('%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f%-10.4f\n'
                                    % (eigen_val[i], file1_data[0], file1_data[1],
                                       (file1_data[2] + file1_data[4] + file1_data[6]),
                                       (file1_data[3] + file1_data[5] + file1_data[7]),
                                       (file1_data[8] + file1_data[10] + file1_data[12] +
                                        file1_data[14] + file1_data[16]),
                                       (file1_data[9] + file1_data[11] + file1_data[13] +
                                        file1_data[15] + file1_data[17]),
                                       (file1_data[18] + file1_data[20] + file1_data[22] +
                                        file1_data[24] + file1_data[26] + file1_data[28] +
                                        file1_data[30]),
                                       (file1_data[19] + file1_data[21] + file1_data[23] +
                                        file1_data[25] + file1_data[27] + file1_data[29] +
                                        file1_data[31])))

    for atom in atom_names:
        os.system('rm ./%s/%s_l' % (atom, atom))
else:
    print '我不认识DOSCAR的数据结构，请检查。'
    exit()

# 下面这段程序将DOSCAR的数据按原子类别,自旋上下,lm分开
for n in range(NEDOS):
    for m in range(len(m_phases)):
        for k, atom in enumerate(atom_names):
            val = [0] * len(m_phases)
            for l in range(atom_numbers[k]):
                index = m + ((l + (sum(atom_numbers) - sum(atom_numbers[k:])))
                             * NEDOS + n) * len(m_phases)
                val[m] += dos_data[index]
            with open('./%s/%s_lm' % (atom, atom), 'a+') as atom_file:
                atom_file.write('%-10.4f' % val[m])
                if m == len(m_phases) - 1:
                    atom_file.write('\n')
for atom in atom_names:
    with open('./%s/%s_lm' % (atom, atom), 'r') as file1:
        with open('./%s/%s_lm.dat' % (atom, atom), 'w') as file2:
            for i in range(NEDOS):
                file2.write('%-10.4f%s' % (eigen_val[i], file1.readline()))
for atom in atom_names:
    os.system('rm ./%s/%s_lm' % (atom, atom))

print 'DOSCAR数据处理完毕。ENJOY.'
print '耗时%dS' % (time.time() - start_time)
