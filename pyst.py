import inspect
currtestr = []
class TestCase:
    def assertEquals(self, a, b):
        if a == b:
            self.add_result(0);  # Everything OK
        else:
            self.add_result(1);  # This is not equal

    def assertSame(self, a, b):
        if a is b:
            self.add_result(0);  # Everything OK
        else:
            self.add_result(1);  # This is not equal

    def assertMore(self, a, b):
        if a > b:
            self.add_result(0);  # Everything OK
        else:
            self.add_result(1);  # This is not equal

    def assertLess(self, a, b):
        if a < b:
            self.add_result(0);  # Everything OK
        else:
            self.add_result(1);  # This is not equal

    def assertNone(self, a):
        if a is None:
            self.add_result(0);  # Everything OK
        else:
            self.add_result(1);  # This is not equal

    def add_result(self, r):
        currtestr.append(r)

def test_cases(a):
    if isinstance(a, TestCase):
        methods = inspect.getmembers(a, predicate=inspect.ismethod)
        for tmethod in methods:
            if tmethod[0].startswith('test_'):
                getattr(a, tmethod[0])()
                print("Result for " + tmethod[0] + ": " + str(currtestr))

    else:
        raise TypeError
