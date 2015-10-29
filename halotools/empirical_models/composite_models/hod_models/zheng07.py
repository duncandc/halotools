# -*- coding: utf-8 -*-
"""

Module containing the HOD-style composite model published in Zheng et al. (2007)

"""
from __future__ import (
    division, print_function, absolute_import, unicode_literals)

import numpy as np

from ... import model_defaults
from ...occupation_models import zheng07_components
from ...phase_space_models import NFWPhaseSpace, TrivialPhaseSpace
from ... import factories

from ....sim_manager import FakeSim


__all__ = ['return_zheng07_model_dictionary']


def return_zheng07_model_dictionary(
    threshold = model_defaults.default_luminosity_threshold, **kwargs):
    """ Blueprint for an HOD-style based on Zheng et al. (2007), arXiv:0703457. 

    There are two populations, centrals and satellites. 
    Central occupation statistics are given by a nearest integer distribution 
    with first moment given by an ``erf`` function; the class governing this 
    behavior is `~halotools.empirical_models.occupation_components.Zheng07Cens`. 
    Central galaxies are assumed to reside at the exact center of the host halo; 
    the class governing this behavior is `~halotools.empirical_models.TrivialPhaseSpace`. 

    Satellite occupation statistics are given by a Poisson distribution 
    with first moment given by a power law that has been truncated at the low-mass end; 
    the class governing this behavior is `~halotools.empirical_models.occupation_components.Zheng07Sats`; 
    satellites in this model follow an (unbiased) NFW profile, as governed by the 
    `~halotools.empirical_models.NFWPhaseSpace` class. 

    This composite model is built by the `~halotools.empirical_models.factories.HodModelFactory`.

    Parameters 
    ----------
    threshold : float, optional 
        Luminosity threshold of the galaxy sample being modeled. 
        Default is set in the `~halotools.empirical_models.model_defaults` module. 

    Returns 
    -------
    model_blueprint : dict 
        Dictionary of keywords to be passed to 
        `~halotools.empirical_models.factories.HodModelFactory`

    Examples 
    --------

    >>> model_blueprint = return_zheng07_model_dictionary()
    >>> model_instance = factories.HodModelFactory(**model_blueprint)

    The default settings are set in the `~halotools.empirical_models.model_defaults` module. 
    To load a model based on a different threshold, use the ``threshold`` keyword argument:

    >>> model_blueprint = return_zheng07_model_dictionary(threshold = -21)
    >>> model_instance = factories.HodModelFactory(**model_blueprint)

    This call will create a model whose parameter values are set according to the best-fit 
    values given in Table 1 of arXiv:0703457. 

    For this model, you can also use the following syntax candy, 
    which accomplishes the same task as the above:

    >>> model_instance = factories.HodModelFactory('zheng07', threshold = -21)

    As with all instances of the `~halotools.empirical_models.HodModelFactory`, 
    you can populate a mock with one line of code: 

    >>> model_instance.populate_mock(simname = 'bolshoi', redshift = 0) # doctest: +SKIP

    """

    ####################################
    ### Build subpopulation blueprint for centrals
    subpopulation_blueprint_centrals = {}

    # Build the `occupation` feature
    centrals_occupation = zheng07_components.Zheng07Cens(threshold = threshold, **kwargs)

    # Build the `profile` feature
    centrals_profile = TrivialPhaseSpace(**kwargs)

    ####################################
    ### Build subpopulation blueprint for satellites
    subpopulation_blueprint_satellites = {}

    # Build the occupation model
    satellites_occupation = zheng07_components.Zheng07Sats(threshold = threshold, **kwargs)
    satellites_occupation._suppress_repeated_param_warning = True

    # Build the profile model
    satellites_profile = NFWPhaseSpace(**kwargs)    


    return ({'centrals_occupation': centrals_occupation, 
        'centrals_profile': centrals_profile, 
        'satellites_occupation': satellites_occupation, 
        'satellites_profile': satellites_profile})




    


    
