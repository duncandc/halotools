#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)

from unittest import TestCase
from astropy.tests.helper import pytest

import numpy as np 
from copy import copy 

from ...factories import HodModelFactory, PrebuiltHodModelFactory

from ....sim_manager import FakeSim
from ....custom_exceptions import HalotoolsError

__all__ = ['TestHodModelFactory']

class TestHodModelFactory(TestCase):
    """ Class providing tests of the `~halotools.empirical_models.SubhaloModelFactory`. 
    """

    def setUp(self):
        """ Pre-load various arrays into memory for use by all tests. 
        """
        pass

    def test_empty_arguments(self):
        with pytest.raises(HalotoolsError) as err:
            model = HodModelFactory()
        substr = "You did not pass any model features to the factory"
        assert substr in err.value.message

    def test_populate_mock1(self):
        model = PrebuiltHodModelFactory('zheng07')
        halocat = FakeSim()
        model.populate_mock(halocat = halocat)
        model.populate_mock(halocat = halocat)
        model.populate_mock(simname = halocat.simname, 
            redshift = halocat.redshift, 
            halo_finder = halocat.halo_finder, 
            version_name = halocat.version_name)

        with pytest.raises(HalotoolsError) as err:
            model.populate_mock(simname = 'bolshoi')
        substr = "Inconsistency between the simname already bound to the existing mock"
        assert substr in err.value.message

        with pytest.raises(HalotoolsError) as err:
            model.populate_mock(simname = halocat.simname, redshift = 4.)
        substr = "Inconsistency between the redshift already bound to the existing mock"
        assert substr in err.value.message

        with pytest.raises(HalotoolsError) as err:
            model.populate_mock(simname = halocat.simname, 
                redshift = halocat.redshift, 
                halo_finder = 'Jose Canseco')
        substr = "Inconsistency between the halo-finder "
        assert substr in err.value.message

        with pytest.raises(HalotoolsError) as err:
            model.populate_mock(simname = halocat.simname, 
                redshift = halocat.redshift, 
                halo_finder = halocat.halo_finder, 
                version_name = 'mo biscuit')
        substr = "Inconsistency between the version_name "
        assert substr in err.value.message

        halocat_redshift2 = FakeSim(redshift = 2.)
        with pytest.raises(HalotoolsError) as err:
            model.populate_mock(halocat = halocat_redshift2)
        substr = "Inconsistency between the redshift already bound to the existing mock"
        assert substr in err.value.message

    def test_Num_ptcl_requirement(self):
        """ Demonstrate that passing in varying values for 
        Num_ptcl_requirement results in the proper behavior. 
        """
        model = PrebuiltHodModelFactory('zheng07')
        halocat = FakeSim()
        actual_mvir_min = halocat.halo_table['halo_mvir'].min()

        model.populate_mock(halocat = halocat)
        default_mvir_min = model.mock.particle_mass*model.mock.Num_ptcl_requirement
        # verify that the cut was applied
        assert np.all(model.mock.halo_table['halo_mvir'] > default_mvir_min)
        # verify that the cut was non-trivial
        assert np.any(halocat.halo_table['halo_mvir'] < default_mvir_min)

        del model.mock 
        model.populate_mock(halocat = halocat, Num_ptcl_requirement = 0.)
        assert model.mock.Num_ptcl_requirement == 0.
        assert np.any(model.mock.halo_table['halo_mvir'] < default_mvir_min)





    def tearDown(self):
        pass