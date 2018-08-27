#!/usr/bin/python
# coding:utf-8


"""This program can rewrite p4vasp output file band data."""

print '\nThis program can rewrite p4vasp output file band data.\n'
print 'P4vasp always move fermi level to 0.\n'


def get_nkpoints(f_p4v_band, f_length):
    """Return number of kpoints."""
    with open(f_p4v_band, 'r') as f_p4v_band_file:
        line_i = 0
        for get_nkpoints_i in range(f_length):
            if f_p4v_band_file.readline() != '\n':
                line_i += 1
            else:
                break
    return line_i


def get_nbands(f_p4v_band, ff_length):
    """Return number of bands."""
    with open(f_p4v_band, 'r') as f_p4v_band_file:
        line_ii = 0
        for get_nbands_i in range(ff_length):
            if len(f_p4v_band_file.readline().split()) <= 2:
                line_ii += 1
            else:
                break
    f_nkpoints = get_nkpoints(f_p4v_band, ff_length) + 1
    f_nbands = line_ii / f_nkpoints
    return f_nbands


p4v_band = raw_input('Please input origin file name:')

####################################################
# get line number of origin file
length = len(['' for line in open(p4v_band, 'r')])
####################################################

# get numbers of kpoints and bands
nkpoints = get_nkpoints(p4v_band, length)
nbands = get_nbands(p4v_band, length)
print 'You plot %d bands with %d kpoints.\n' % (nbands, nkpoints)

# get projected band numbers
p_bands = length / ((nkpoints + 1) * nbands) - 1

# list energy_date save energies
kpoints_data = []
# list band_line_data save band data
energy_data = []
# list band_symbol save band symbol sizes
band_symbol = []

# read data
# read kpoints
with open(p4v_band, 'r') as p4v_band_file:
    for i in range(nkpoints):
        kpoints_data.append(p4v_band_file.readline().split()[0])
# read energy
with open(p4v_band, 'r') as p4v_band_file:
    for j in range(nbands):
        for k in range(nkpoints):
            energy_data.append(p4v_band_file.readline().split()[1])
        p4v_band_file.readline()
# read symbol
with open(p4v_band, 'r') as p4v_band_file:
    for l in range(nbands):
        for m in range(nkpoints):
            p4v_band_file.readline()
        p4v_band_file.readline()
    for n in range(p_bands):
        for o in range(nbands):
            for p in range(nkpoints):
                band_symbol.append(p4v_band_file.readline().split()[2])
            p4v_band_file.readline()

# write data
p4vasp_band = raw_input('Please input file name which you want to save band data (default: %s.out):' % p4v_band)
if p4vasp_band == '':
    p4vasp_band = '%s.out' % p4v_band
else:
    pass
with open(p4vasp_band, 'w') as p4vasp_band_file:
    for i in range(nbands):
        for j in range(nkpoints):
            p4vasp_band_file.write('%-12s' % kpoints_data[j])
            p4vasp_band_file.write('%-12s' % energy_data[i * nkpoints + j])
            for k in range(p_bands):
                p4vasp_band_file.write('%-12s' % band_symbol[k * nbands * nkpoints + i * nkpoints + j])
            p4vasp_band_file.write('\n')
        p4vasp_band_file.write('\n')
    print '\nI have save band data to %s.\n' % p4vasp_band

print 'Add tags (ex: #KPOINTS ENERGY Si s Si p) at head of %s to remind you later.\n' % p4vasp_band
