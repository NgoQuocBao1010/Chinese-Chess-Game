a = [("a", 1), ("b", 2)]

test = dict( ele for ele in a )

def foo(*args, **kwargs):
    print(kwargs['test'])


foo(test=4)