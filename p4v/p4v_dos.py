#!/usr/bin/python
# coding:utf-8

import os

"""This program can split p4vasp output file dos data."""

print 'This program can split p4vasp output file dos data.\n'


def get_nedos():
    """This function get NEDOS from OUTCAR."""
    os.system('grep NEDOS OUTCAR')
    f_nedos = raw_input('\nPlease input NEDOS (default: 301):')
    if f_nedos == '':
        f_nedos = 301
    else:
        f_nedos = int(f_nedos)
    return f_nedos


p4v_dos = raw_input('Please input origin file name:')

####################################################
# get line number of origin file
length = len(['' for line in open(p4v_dos, 'r')])
print '\n%s has %d lines\n' % (p4v_dos, length)
####################################################

nedos = get_nedos()

# get number of dos lines
dos_line = length / nedos
print 'You plot %d dos lines.\n' % dos_line

# list energy_date save energies
energy_data = []
# list dos_line_data save dos data
dos_line_data = []

# read data
with open(p4v_dos, 'r') as p4v_dos_file:
    for i in range(nedos):
        energy_data.append(p4v_dos_file.readline().split()[0])
with open(p4v_dos, 'r') as p4v_dos_file:
    for i in range(dos_line):
        for j in range(nedos):
            dos_line_data.append(p4v_dos_file.readline().split()[1])
        p4v_dos_file.readline()

# write data
p4v_dos_split = raw_input('Please input file name which you want to save dos data (default: p4vasp_band):')
if p4v_dos_split == '':
    p4v_dos_split = 'p4vasp_band'
else:
    pass
with open(p4v_dos_split, 'w') as p4v_dos_split_file:
    for i in range(nedos):
        p4v_dos_split_file.write('%-12s' % energy_data[i])
        for j in range(dos_line):
            p4v_dos_split_file.write('%-12s' % dos_line_data[j * nedos + i])
        p4v_dos_split_file.write('\n')
    print '\nI have save dos data to %s. ENJOY!\n' % p4v_dos_split
