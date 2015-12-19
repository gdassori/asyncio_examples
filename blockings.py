import asyncio
import time


def blocking(arg, cb, eb):
    time.sleep(arg)
    cb('done')

def blockingerr(arg, cb, eb):
    time.sleep(arg)
    try:
        raise Exception()
    except Exception as e:
        eb('error')

def returnblocking(arg):
    time.sleep(arg)
    return 'return'

def raiseexception(arg):
    time.sleep(arg)
    raise ValueError('excepti0n')

def callback(res, cb):
    print('cb: {}'.format(res))
    cb()

def run_blocking_1(loop):
    cb = lambda x: callback(x, lambda: run_blocking_1(loop))
    task = lambda: blocking(3, cb, None)
    loop.run_in_executor(None, task)

def run_blocking_2(loop):
    cb = lambda x: callback(x, lambda: run_blocking_2(loop))
    task = lambda: blockingerr(1, None, cb)
    loop.run_in_executor(None, task)

def run_blocking_3(loop):
    task = lambda: returnblocking(5)
    q = loop.run_in_executor(None, task)
    cb = lambda x: callback(x, lambda: run_blocking_3(loop))
    q.add_done_callback(lambda x: cb(x.result()))

def run_blocking_4(loop):
    def inspect(x, cb):
        if x.exception():
            cb(x.exception())
        else:
            cb(x.result())

    task = lambda: raiseexception(10)
    q = loop.run_in_executor(None, task)
    cb = lambda x: inspect(x, lambda x: callback(x, lambda: run_blocking_4(loop)))
    q.add_done_callback(lambda x: cb(x))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run_blocking_1(loop)
    run_blocking_2(loop)
    run_blocking_3(loop)
    run_blocking_4(loop)
    loop.set_exception_handler(None)
    loop.run_forever()
