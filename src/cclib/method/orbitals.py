# -*- coding: utf-8 -*-
#
# This file is part of cclib (http://cclib.github.io), a library for parsing
# and interpreting the results of computational chemistry packages.
#
# Copyright (C) 2016, the cclib development team
#
# The library is free software, distributed under the terms of
# the GNU Lesser General Public version 2.1 or later. You should have
# received a copy of the license along with cclib. You can also access
# the full license online at http://www.gnu.org/copyleft/lgpl.html.

"""Analyses related to orbitals."""

import logging

import numpy

from .calculationmethod import Method


class Orbitals(Method):
    """A class for orbital related methods."""

    def __init__(self, data, progress=None, \
                 loglevel=logging.INFO, logname="Log"):

        # Call the __init__ method of the superclass.
        super(Orbitals, self).__init__(data, progress, loglevel, logname)

    def __str__(self):
        """Return a string representation of the object."""
        return "Orbitals"

    def __repr__(self):
        """Return a representation of the object."""
        return "Orbitals"

    def closed_shell(self):
        """Return Boolean indicating if system is closed shell."""

        # If there is only one HOMO, the system is closed-shell by
        # definition.
        if len(self.data.homos) == 1:
            return True
        # Both unrestricted and restricted open-shell calculations
        # may have two HOMOs.
        else:
            # In the case where the two HOMOs are different (any spin
            # multiplicity other than singlet), the system is
            # open-shell by definition.
            if self.data.homos[0] != self.data.homos[1]:
                return False
            # In the case where the two HOMOs are identical, it is not
            # sufficient to just check MO energies. The way we
            # differentiate between a restricted calculation run as
            # unrestricted and a broken-symmetry singlet is the
            # difference in MO coefficients.
            else:
                precision = 10e-6
                return numpy.allclose(*self.data.mocoeffs, atol=precision)


if __name__ == "__main__":
    import doctest, orbitals
    doctest.testmod(orbitals, verbose=False)
