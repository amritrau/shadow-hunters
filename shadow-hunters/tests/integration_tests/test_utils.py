import pytest
from utils import make_hash_sha256

# test_utils.py


def test_make_hash_sha256():
    w = {'a': ['b', None, dict(c=dict(), d=(1, 2))], (3, 4): 'e'}
    x = {'a': ['b', None, dict(c=dict(), d=(1, 2))], (3, 4): 'e'}
    y = {'b': ['b', None, dict(c=dict(), d=(1, 2))], (3, 4): 'e'}
    z = {(3, 4): 'e', 'b': ['b', None, dict(c=dict(), d=(1, 2))]}
    assert make_hash_sha256(w) == make_hash_sha256(x)
    assert make_hash_sha256(x) != make_hash_sha256(y)
    assert make_hash_sha256(y) != make_hash_sha256(z)
