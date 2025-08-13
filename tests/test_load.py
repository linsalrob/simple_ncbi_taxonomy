"""
A test the load functions
"""

from simple_ncbi_taxonomy import load_ncbi_taxonomy, read_names

__author__ = 'Rob Edwards'


def test_load_names():
    names, gbknames = read_names()
    print(names['8276'].__dict__)
    assert names['8276'].get_name() == 'Pantodon buchholzi'




