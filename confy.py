import json
import collections
import os.path

class Confy(collections.MutableMapping):
    """A dictionary backed by a json file, serves as a replacement to ini/config files. Use like any other dict, call .save() to save. 

    Initialize it with a filename, the backing file will be created if it didn't previously exist,
    otherwise, the contents of the file will be loaded into the dict.

    save using confy.save()
    """

    def __init__(self, filename, *args, **kwargs):
        self.store = dict()
        self.filename = filename
        self.update(dict(*args, **kwargs))  # use the free update to set keys

        if os.path.isfile(self.filename):
            # if storage exists, load it into this dict
            with open(self.filename) as f:
                self.store = json.load(f)
        else:
            # if storage doesn't exist, create it
            with open(self.filename, 'w') as f:
                f.write("{}") # write an empty dictionary to the file

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f, indent=4)