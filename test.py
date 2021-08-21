class A:
    def doSth(self):
        print("I do something")

        return None


class B(A):
    def doSth(self):
        super().doSth()

        print("Do sth after")
    


b = B()
b.doSth()