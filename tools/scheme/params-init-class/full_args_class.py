# -*- coding: UTF-8 -*-
import inspect


class FullArgsClass(object):
    """
    Use 'self.attributes' to observe the
    corresponding variable-length arguments.
    """
    def __init__(self, x, y, z, *args, **kwargs):
        # Collect keys for all properties
        self.attributes = dict()

        # Get positional params dynamically
        arg_spec = inspect.getfullargspec(self.__class__)
        param_fixed = arg_spec.args
        param_fixed.pop(0)
        if param_fixed:
            for i in param_fixed:
                self.__setattr__(i, eval(i))
            self.attributes.update({'fixed': param_fixed})

        # Get *args dynamically
        if arg_spec.varargs:
            param_args = []
            for i in range(1, len(args)+1):
                name = f"{arg_spec.varargs.lower()}{i:02}"
                param_args.append(name)
                self.__setattr__(name, args[i-1])
            self.attributes.update({'args': param_args})

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

    def keys(self):
        for i, j in self.attributes.items():
            if i == "fixed":
                fixed = ", ".join(j)
            elif i == "args":
                args = ", ".join(j)
            elif i == "kwargs":
                kwargs = ", ".join(j)
        width = max(len(fixed), len(args), len(kwargs))
        width += 10 - width % 10
        line = "─" * width * 2
        print("\n" + line)
        print(f"{'NAME':^{width}}│{'KEYS':^{width-1}}")
        print(line)
        print(f"{'this':<{width}}│{'self':>{width-1}}")
        print(f"{'fixed':<{width}}│{fixed:>{width-1}}")
        print(f"{'*args':<{width}}│{args:>{width-1}}")
        print(f"{'**kwargs':<{width}}│{kwargs:>{width-1}}")
        print(line)
        print("Syntax Reference: ")
        print("\t# Variable parameters of cls __init__ method.")
        print(f"\tdef __init__(self, {fixed}, *args, **kwargs):\n\t\tpass")
        print(line + "\n")



def unit_test():
    print("\n单元测试: ")
    # print(FullArgsClass.__doc__)
    # 实例化对象
    args = ["option1", "option2", "option3"]
    kwargs = {"foo": "value1", "bar": "value2"}
    obj = FullArgsClass('number1', 'number2', 'number3', *args, **kwargs)
    # 使用keys方法，获取val列表
    obj.keys()
    # 测试对象属性的获取
    print("结果: ")
    print("1. %s 固定位置参数中 %s 实例变量的值为 %s" % ("fixed", "obj.x", obj.x))
    print("2. {0} 可变元祖参数中 {1} 实例变量的值为 {2}".format("*args", "obj.args01", obj.args01))
    print(f"3. **kwargs 可变map键值对参数中 obj.foo 实例变量的值为 {obj.foo}")


if __name__ == '__main__':
    unit_test()

