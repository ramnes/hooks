import functools


class Hook(object):

    def __init__(self, hook, func_name, when):
        self.hook = hook
        self.when = when
        self.func_name = func_name
        self.func = None

    def __get__(self, instance, cls):
        print("in __get__")
        func = getattr(instance, self.func_name)

        @functools.wraps(func)
        def _before(*args, **kwargs):
            self.hook(instance, *args, **kwargs)
            return func(*args, **kwargs)

        @functools.wraps(func)
        def _after(*args, **kwargs):
            results = func(instance, *args, **kwargs)
            return self.hook(*results)

        self.func = locals()["_" + self.when]
        self.instance = instance

        setattr(self.instance, self.func_name, self.func)
        return self

    def __call__(self, *args, **kwargs):
        return self.hook(self.instance, *args, **kwargs)


def before(func_name):
    def __inner(hook):
        return Hook(hook, func_name, "before")
    return __inner
