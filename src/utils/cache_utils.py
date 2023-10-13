import pickle, functools
from cachetools import TTLCache
from enum import Enum
from datetime import datetime, timedelta
from exceptions import Expired


class CacheVal:
    def __init__(self, value, expires_in):
        self.value = value
        self._expiration = datetime.now() + timedelta(seconds=expires_in)

    def is_expired(self):
        return datetime.now() > self._expiration
    
    def set_was_cached(self,  boolean):
        self.value.was_cached = boolean
    
class CacheDict(dict):
    
    def __getitem__(self, key):
        item = dict.__getitem__(self, key)
        if key in self and isinstance(item, CacheVal):
            if item.is_expired():
                del self[key]
                raise Expired
            item.set_was_cached(True)
            return item.value
        return item #shouldnt be returned

    def __setitem__(self, key, value):
        if isinstance(value, CacheVal):
            value.set_was_cached(False)
            dict.__setitem__(self, key, value)
        else:
            try:
                cache_val = CacheVal(*value)
                cache_val.set_was_cached(False)
                dict.__setitem__(self, key, cache_val)
            except Exception as e:
                raise Exception(f'cache set error: {e}')
    

def load_pickle(reset=False):
    if reset:
        return CacheDict()
    try:
        with open(f'cache.pickle', 'rb') as f:
           return pickle.load(f)
    except FileNotFoundError:
        return CacheDict()

def dump_pickle(d):
    with open(f'cache.pickle', 'wb') as f:
        pickle.dump(d, f)

def reset_cache():
    with open(f'cache.pickle', 'wb') as f:
        pickle.dump(CacheDict(), f)


def cached(cache, key_str):
    """ decorator to use cache on function. Function must return (value, expires_in: int) or similar
    Args:
        cache (CacheDict): cache to be used
        key_str (str): Name of the key identifying value
    """
    def decorator(func):
        functools.wraps(func)
        def wrapper(*args):
            if isinstance(cache, CacheDict):
                try:
                    value = cache[key_str]
                    return value
                except (Expired, KeyError):
                    val = func(*args)
                    cache[key_str] = val
                    dump_pickle(cache) #TODO consider not dumping every update
                    return val[0] #TODO improve later - dict __get_item__ is setting variable was_cached
            
            else: raise Exception('not CacheDict')
        return wrapper
    return decorator