#!/usr/bin/python
# coding:utf-8

import os

"""This program can get eigenvalue(N), see Phys. Rev. B 80, 085202 (2009), eq(2) for details."""


def get_ispin(outcar):
    """Return ISPIN read from OUTCAR"""
    os.system("grep 'ISPIN' %s | awk '{print $3}' > .ispin" % outcar)
    with open('.ispin', 'r') as ispin_file:
        f_ispin = int(ispin_file.readline().split()[0])
    return f_ispin


def get_nelect(outcar):
    """Return NELECT read from OUTCAR"""
    os.system("grep 'NELECT' %s | awk '{print $3}' > .nelect" % outcar)
    with open('.nelect', 'r') as nelect_file:
        f_nelect = float(nelect_file.readline().split()[0])
    return f_nelect


def get_nkpoints(outcar):
    """Return NKPOINTS read from OUTCAR"""
    os.system("grep 'irreducible' %s | awk '{print $2}' > .nkpoints" % outcar)
    with open('.nkpoints', 'r') as nkpoints_file:
        f_nkpoints = int(nkpoints_file.readline().split()[0])
    return f_nkpoints


def get_kpoints_weight(outcar, f_nkpoints):
    """Return KPOINTS weight and weight sum read from OUTCAR"""
    os.system("grep -A %s 'irreducible' %s | tail -n %s | awk '{print $4}' > .weight"
              % (str(f_nkpoints + 3), outcar, str(f_nkpoints)))
    # list "weight" save weights of kpoints
    f_weight = []
    with open('.weight', 'r') as weight_file:
        for f_i in range(f_nkpoints):
            f_weight.append(weight_file.readline().split()[0])
    os.system("grep -A %s 'irreducible' %s | tail -n %s | awk '{print $4}'| paste -sd + | bc > .weight_sum"
              % (str(f_nkpoints + 3), outcar, str(f_nkpoints)))
    with open('.weight_sum', 'r') as weight_sum_file:
        f_weight_sum = weight_sum_file.readline().split()[0]
    return f_weight_sum, f_weight


def get_eig(outcar, f_nkpoints, f_spin, f_band_no):
    """Return eigenvalue of kpoints"""
    if f_spin == 1:
        os.system("grep '  %s  ' %s | head -n %s | awk '{print $2}' > .eig"
                  % (str(f_band_no), outcar, str(f_nkpoints)))
    else:
        os.system("grep '  %s  ' %s | tail -n %s | awk '{print $2}' > .eig"
                  % (str(f_band_no), outcar, str(f_nkpoints)))
    f_eig = []
    with open('.eig', 'r') as eig_file:
        for f_j in range(f_nkpoints):
            f_eig.append(eig_file.readline().split()[0])
    return f_eig


print '\nThis program can get eigenvalue(N), see Phys. Rev. B 80, 085202 (2009), eq(2) for details.\n'
ispin = get_ispin('OUTCAR')
nelect = get_nelect('OUTCAR')
nkpoints = get_nkpoints('OUTCAR')
weight_sum, weight = get_kpoints_weight('OUTCAR', nkpoints)
print 'ISPIN = %d, NELECT = %f\n' % (ispin, nelect)
band_no = int(raw_input('Please input band NO.(Hint: NELECT/2):\n'))
spin = int(raw_input('Please input spin component (Hint 1 or 2):\n'))
eig = get_eig('OUTCAR', nkpoints, spin, band_no)
eigenvalue = 0
for i in range(nkpoints):
    eigenvalue = eigenvalue + float(eig[i]) * float(weight[i])
eigenvalue_norm = eigenvalue / float(weight_sum)
print 'Eigenvalue of band %d spin component %d is %f eV.\n' % (band_no, spin, eigenvalue_norm)
