from collections import OrderedDict
from pylev import levenshtein

# support for Python 2 and 3
try:
    import builtins
    basestring = unicode = str
except ImportError:
    import __builtin__ as builtins

"""
TODO: 

- allow people to specify what fields they want as indexes
- check for uniqueness (optionally) on entry, not on retrieval
- optionally, specify a field or view function to use when 
returning an item by name
"""

def get(obj, name, lower=False):
    if isinstance(obj, dict):
        value = obj.get(name)
    else:
        value = getattr(obj, name)

    if lower:
        return value.lower()
    else:
        return value

def noop(value):
    return value

def contains(a, b):
    return a.lower() in b.lower()

def equals(a, b):
    return a == b

def iequals(a, b):
    return equals(a.lower(), b.lower())

def apply(fn, l, applicator):
    result = applicator(fn, l)
    cls = l.__class__
    return cls(
        result, 
        indices=l.indexed_on, 
        facet=l.facet, 
        unique=l.unique, 
        fuzzy=l.fuzzy, 
        name=l.name, 
        )

def map(fn, l):
    return apply(fn, l, builtins.map)

def filter(fn, l):
    return apply(fn, l, builtins.filter)


class List(list):
    def __init__(self, items, indices=[], facet=noop, unique=True, fuzzy=False, insensitive=False, name='items'):
        self.name = name
        self.indices = []
        self.indexed_on = indices
        self.unique = unique
        self.fuzzy = fuzzy
        self.insensitive = insensitive
        self.keys = set()

        if isinstance(facet, basestring):
            self.facet = lambda obj: obj[facet]
        else:
            self.facet = facet

        # we need to loop through the items once for every index, so 
        # to avoid problems with iterators, let's make sure items is 
        # a list
        items = list(items)

        for name in indices:
            index = OrderedDict([(get(v, name, lower=insensitive), v) for v in items])
            self.indices.append(index)

            if self.unique:
                intersection = self.keys.intersection(index.keys())
                if intersection:
                    keys = ", ".join(intersection)
                    raise KeyError("Key already indexed: {}".format(keys))

        super(List, self).__init__(items)

    @property
    def cmp(self):
        if self.fuzzy:
            return contains
        elif self.insensitive:
            return iequals
        else:
            return equals

    def suggest(self, key, distance=3):
        suggestions = set()
        for index in self.indices:
            for candidate in index:
                if levenshtein(key, candidate) <= distance:
                    suggestions.add(index[candidate])
        return suggestions


    def __getitem__(self, key):
        if isinstance(key, int):
            return super(List, self).__getitem__(key)
        else:
            value = self.get(key)

            if value:
                return value
            else:
                message = "Cannot find {key} among the available {name}.".format(
                    key=key, name=self.name)
                suggestions = ", ".join(
                    [unicode(suggestion) for suggestion in self.suggest(key)])
                if len(suggestions):
                    suggestions = " Did you mean: {}?".format(suggestions)
                raise KeyError(message + suggestions)                

    def get(self, key, default=None):
        for index in self.indices:
            for candidate in index:
                if self.cmp(key, candidate):
                    found = index[candidate]
                    return self.facet(found)
        return default

    def index(self, key):
        for index in self.indices:
            for i, candidate in enumerate(index):
                if self.cmp(key, candidate):
                    return i
        raise ValueError(key + " is not in list")
