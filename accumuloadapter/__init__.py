"""
    AccumuloAdapter
    ~~~~~~~~~~~~~~~

    AccumuloAdapter provides tools to interface Accumulo databases in a fast,
    memory-efficient way.
"""
from __future__ import absolute_import

import sys
import os
import pytest

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


from accumuloadapter.core.AccumuloAdapter import AccumuloAdapter
from accumuloadapter.lib.errors import (AdapterException, AdapterIndexError,
                                        ArgumentError, ConfigurationError,
                                        DataIndexError, DataTypeError,
                                        InternalInconsistencyError, NoSuchFieldError,
                                        ParserError, SourceError, SourceNotFoundError)


def test(host='localhost', user='root', password='GisPwd', verbose=True):
    test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests')        
    accumulo_test_script = 'test_AccumuloAdapter.py'
    args = []
    args.append(os.path.join(test_dir, accumulo_test_script))
    args.append('--acc_host {0}'.format(host))
    args.append('--acc_user {0}'.format(user))
    if password is not None:
        args.append('--acc_password {0}'.format(password))
    if verbose:
        args.append('-v')

    result = pytest.main(' '.join(args))
    if result == 0:
        return True
    return False
