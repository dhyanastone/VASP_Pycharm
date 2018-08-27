#!/usr/bin/python


def center_atom():
    """Return coordinates of center atom"""
    x = float(raw_input('Input x of center atom:\n'))
    y = float(raw_input('Input y of center atom:\n'))
    z = float(raw_input('Input z of center atom:\n'))
    return [x, y, z]


print "\nSpecify one atom, say A, and a distance in angstrom, say d." \
      "I can produce structure including atoms, say B, with d(A-B) < d.\n"

print "Mind: I can only read POSCAR or CONTdCAR.\n"

center = center_atom()
print 'OK! The center will be (%f, %f, %f)\n' % (center[0], center[1], center[3])
