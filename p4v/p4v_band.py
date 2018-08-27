#!/usr/bin/python
# coding:utf-8

import os

"""This program can split p4vasp output file band data."""

print 'This program can split p4vasp output file band data.\n'
print 'P4vasp always move fermi level to 0.\n'


def get_nkpoints(f_p4v_band):
    """Return number of kpoints."""
    with open(f_p4v_band, 'r') as f_p4v_band_file:
        line_i = 0
        if f_p4v_band_file.readline():
            line_i += 1
    return line_i


def get_nbands(f_p4v_band):
    """Return number of bands."""
    with open(f_p4v_band, 'r') as f_p4v_band_file:
        line_ii = 0
        if len(f_p4v_band_file.readline().split()) != 3:
            line_ii += 1
    f_nkpoints = get_nkpoints(f_p4v_band) + 1
    f_nbands = line_ii / f_nkpoints
    return f_nbands


p4v_band = raw_input('Please input origin file name:')

####################################################
# get line number of origin file
length = len(['' for line in open(p4v_band, 'r')])
print '\n%s has %d lines\n' % (p4v_band, length)
####################################################

# get numbers of kpoints and bands
nkpoints = get_nkpoints(p4v_band)
nbands = get_nbands(p4v_band)
print 'You plot %d bands with %d kpoints.\n' % (nkpoints, nbands)

# get projected band numbers
p_bands = length/((nkpoints + 1) * nbands) - 1

# list energy_date save energies
energy_data = []
# list band_line_data save band data
band_line_data = []
# list band_symbol save band symbols
band_symbol = []

# read data
# read kpoints
with open(p4v_band, 'r') as p4v_band_file:
    for i in range(nbands):
        for j in range(nkpoints):
            energy_data.append(p4v_band_file.readline().split()[0])
        p4v_band_file.readline()
# read energy
with open(p4v_band, 'r') as p4v_band_file:
    for i in range(nbands):
        for j in range(nkpoints):
            band_line_data.append(p4v_band_file.readline().split()[1])
        p4v_band_file.readline()
# read symbol


# write data
p4v_dos_split = raw_input('Please input file name which you want to save dos data (default: p4v_dos_split):')
if p4v_dos_split == '':
    p4v_dos_split = 'p4v_dos_split'
else:
    pass
with open(p4v_dos_split, 'w') as p4v_dos_split_file:
    for i in range(nedos):
        p4v_dos_split_file.write('%-12s' % energy_data[i])
        for j in range(dos_line):
            p4v_dos_split_file.write('%-12s' % band_line_data[j * nedos + i])
        p4v_dos_split_file.write('\n')
    print '\nI have save dos data to %s. ENJOY!\n' % p4v_dos_split
