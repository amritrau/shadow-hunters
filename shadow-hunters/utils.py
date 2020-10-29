import hashlib
import base64


def make_hashable(x):
    """Make a generic object hashable.
    From https://stackoverflow.com/questions/5884066/hashing-a-dictionary"""
    if isinstance(x, (tuple, list)):
        return tuple((make_hashable(e) for e in x))
    elif isinstance(x, dict):
        return tuple((k, make_hashable(v)) for k, v in x.items())
    elif isinstance(x, (set, frozenset)):
        return tuple(make_hashable(e) for e in x)

    return x


def make_hash_sha256(x):
    """Hash a dictionary in a platform-independent manner.
    From https://stackoverflow.com/questions/5884066/hashing-a-dictionary"""
    hasher = hashlib.sha256()
    hasher.update(repr(make_hashable(x)).encode())
    return base64.b64encode(hasher.digest()).decode()
