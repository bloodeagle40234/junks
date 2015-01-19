#!/bin/python


class Wrappee(object):
    def __init__(self):
        self.value = 1

    def get_value(self):
        return self.value

if __name__ == '__main__':
    wrappee = Wrappee()
    orig_func = wrappee.get_value

    def wrap_func():
        value = orig_func()
        value += 1
        return value

    wrappee.get_value = wrap_func
    assert wrappee.get_value() == 2
