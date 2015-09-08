import hook


class Foo:

    def bar(self):
        print("barbar")


class FooChild(Foo):

    @hook.before("bar")
    def pre_bar(self):
        print(self.__class__.__name__)
        print("pre_bar")
        

foo = FooChild()
