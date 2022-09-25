## 初始化类的变长参数

> 两个示例，重点介绍 `**kwargs` 在类实例化对象执行 `__init__` 方法时，如何自动解构并动态赋值。

### 知识点

Proper way to use `**kwargs` in Python Class type

```python
When defining classes and instantiating objects in Python, how to deal with the case of 
**kwargs variable-length parameters regarding the __init__ initialization method?

Whenever processing **kwargs with multiple unknown arguments:

  1. Popular method: try to get via kwargs.get('xxx');
  2. Another: Implemented by reflection __setattr__;
```

### 运行结果

```shell
单元测试1: 

────────────────────────────────────────────────────────────
             NAME             │            KEYS             
────────────────────────────────────────────────────────────
this                          │                         self
fixed                         │                      x, y, z
*args                         │       args01, args02, args03
**kwargs                      │                     foo, bar
────────────────────────────────────────────────────────────
Syntax Reference: 
        # Variable parameters of cls __init__ method.
        def __init__(self, x, y, z, *args, **kwargs):
                pass
────────────────────────────────────────────────────────────

结果: 
1. fixed 固定位置参数中 obj.x 实例变量的值为 number1
2. *args 可变元祖参数中 obj.args01 实例变量的值为 option1
3. **kwargs 可变map键值对参数中 obj.foo 实例变量的值为 value1


单元测试2: 

────────────────────
   NAME   │  KEYS   
────────────────────
this      │     self
**kwargs  │ foo, bar
────────────────────

**kwargs The value of the obj.foo instance variable in
the variable map key-value pair parameter is value1.
```
