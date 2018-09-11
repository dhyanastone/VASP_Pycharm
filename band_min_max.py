#!/usr/bin/python
# coding:utf-8

import os

"""This program can get minimum and maximum eigenvalues of band N spin component M."""


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


def get_nkpts_nbands(outcar):
    """Return NKPTS and NBANDS read from OUTCAR"""
    os.system("grep 'NKPTS' %s | awk '{print $4,$15}' > .nkpts_nbands" % outcar)
    with open('.nkpts_nbands', 'r') as nkpts_nbands_file:
        f_nkpts, f_nbands = map(int, nkpts_nbands_file.readline().split())
    return f_nkpts, f_nbands


def get_eig(outcar, f_ispin, f_nkpts, f_nbands, f_spin, f_band_no):
    """Return eigenvalue of kpoints"""
    os.system("grep -A %s 'E-fermi' %s > .eig_file"
              % (str(f_ispin * f_nkpts * (f_nbands + 3) + 6), outcar))
    if f_ispin == 1:
        # To write#################
        pass
        ###########################
    else:
        if f_spin == 1:
            # do not use 'head' to pick, use '-m', search 'grep: write error: Broken pipe' (Evernote)
            os.system("grep '^[ ]*%s  ' .eig_file -m %s | awk '{print $2}' > .eig"
                      % (str(f_band_no), str(f_nkpts)))
        else:
            os.system("grep '^[ ]*%s  ' .eig_file | tail -n %s | awk '{print $2}' > .eig"
                      % (str(f_band_no), str(f_nkpts)))
    f_eig = []
    with open('.eig', 'r') as eig_file:
        for f_j in range(f_nkpts):
            f_eig.append(float(eig_file.readline().split()[0]))
    return f_eig


print "\nThis program can get minimum and maximum eigenvalues of specified band and spin component.\n"
ispin = get_ispin('OUTCAR')
nelect = get_nelect('OUTCAR')
nkpts, nbands = get_nkpts_nbands('OUTCAR')
print 'ISPIN = %d, NELECT = %f, NKPTS = %d, NBANDS = %d\n' % (ispin, nelect, nkpts, nbands)
band_no = int(raw_input('Please input band NO.(Hint: NELECT/2):\n'))
spin = int(raw_input('\nPlease input spin component (Hint: 1 or 2):\n'))
eig = get_eig('OUTCAR', ispin, nkpts, nbands, spin, band_no)
print '\n(minimum, maximum) of band %d spin component %d is (%f, %f) eV.\n' % (band_no, spin, min(eig), max(eig))
os.system("rm -f .eig .eig_file .ispin .nelect .nkpts_nbands")
