class A:
    def __init__(self):
        self.a = 10


class B:
    def __init__(self, a):
        self.A = a


a = A()
a.a = 10
b = B(a)

a.a = 100
print(b.A.a)

import threading

a.a = threading.Event()
print(b.A.a.is_set())
