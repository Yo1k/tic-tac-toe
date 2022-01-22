def eq(cls):
    """ Class decorator providing generic comparison functionality """
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    cls.__eq__ = __eq__
    return cls
