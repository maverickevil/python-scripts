from celeryApp.main import app
from random import choice


@app.task(name="no_args_no_ret")
def no_args_no_ret():
    """ 没有参数，且没有返回值的异步任务 """
    print('类型：无入参且无返回值，任务执行...')


@app.task(name="has_args_no_ret")
def has_args_no_ret(arg1, arg2):
    """ 有参数，但没有返回值的异步任务 """
    print('类型：有入参但无返回值，任务执行...')
    print(f'参数：arg1：{arg1}、arg2：{arg2}')


@app.task(name="no_args_has_ret")
def no_args_has_ret():
    """ 没有参数，但有返回值的异步任务 """
    print('类型：无入参但有返回值，任务执行...')
    return choice((True, False))


@app.task(name="has_args_has_ret")
def has_args_has_ret(arg1, arg2):
    """ 有参数，且有返回值的异步任务 """
    print('类型：有入参且有返回值，任务执行...')
    print(f'参数：arg1：{arg1}、arg2：{arg2}')
    return choice((True, False))

