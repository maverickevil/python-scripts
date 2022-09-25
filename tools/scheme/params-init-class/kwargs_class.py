# -*- coding: UTF-8 -*-
import inspect


class KwargsClass(object):
    """
    Use 'self.attributes' to observe the
    corresponding variable-length arguments.
    """
    def __init__(self, **kwargs):
        # Collect keys for all properties
        self.attributes = dict()

        # Get positional params dynamically
        arg_spec = inspect.getfullargspec(self.__class__)

        # Get **kwargs dynamically
        if arg_spec.varkw:
            param_keys = []
            for k, v in kwargs.items():
                param_keys.append(k)
                self.__setattr__(k, v)
            self.attributes.update({'kwargs': param_keys})

        # View the self member variable
        # self.__repr__()

    def __repr__(self):
        """Debugging: Viewing Class Object Properties"""
        print(self.__dict__)
        return super(self.__class__, self).__repr__()

    @property
    def keys(self):
        for i in self.attributes.values():
            kwargs = ", ".join(i)
        width = len(kwargs)
        width += 10 - width % 10
        line = "─" * width * 2
        report = "\n" + line + f"\n{'NAME':^{width}}│{'KEYS':^{width-1}}\n" + \
                 line + f"\n{'this':<{width}}│{'self':>{width-1}}" + \
                 f"\n{'**kwargs':<{width}}│{kwargs:>{width-1}}\n" + line + "\n"
        return report


def unit_test():
    print("\n单元测试: ")
    # print(KwargsClass.__doc__)
    kwargs = {"foo": "value1", "bar": "value2"}
    obj = KwargsClass(**kwargs)
    # Use the 'keys' method to get a list of vals.
    print(obj.keys)
    # Get test object properties
    print(f"**kwargs The value of the obj.foo instance variable in\n"
          f"the variable map key-value pair parameter is {obj.foo}.")


if __name__ == '__main__':
    unit_test()

