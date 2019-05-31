class PrivateEasyNoneHelper:
    pass


EASY_NONEHELPER = PrivateEasyNoneHelper


def keyValIterator(targetlist):
    for entry in targetlist:
        yield entry["key"], entry["value"]
