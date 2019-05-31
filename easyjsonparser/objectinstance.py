class EasyJSONObjectInstance(object):
    __easy_keys__ = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise RuntimeError("Error during instance object instantiation: "
                                   f"invalid keyword {key} supplied")
            setattr(self, key, val)

    def __repr__(self):
        return "{{{content}}}".format(
            class_name=self.__class__.__name__,
            content=", ".join(f"'{attr}': {repr(getattr(self, attr))}"
                              for attr in self.__easy_keys__ if attr != "__easy_keys__")
        )

    def __str__(self):
        return self.__repr__()
