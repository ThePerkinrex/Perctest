import inspect, os, importlib
currtestr = []
class TestCase:
    def assertEquals(self, a, b):
        if a == b:
            self.add_result(0, 'assertEquals('+str(a)+','+str(b)+')');  # Everything OK
        else:
            self.add_result(1, 'assertEquals('+str(a)+','+str(b)+')');  # This is not equal

    def assertSame(self, a, b):
        if a is b:
            self.add_result(0, 'assertSame('+str(a)+','+str(b)+')');  # Everything OK
        else:
            self.add_result(1, 'assertSame('+str(a)+','+str(b)+')');  # This is not equal

    def assertMore(self, a, b):
        if a > b:
            self.add_result(0, 'assertMore('+str(a)+','+str(b)+')');  # Everything OK
        else:
            self.add_result(1, 'assertMore('+str(a)+','+str(b)+')');  # This is not equal

    def assertLess(self, a, b):
        if a < b:
            self.add_result(0, 'assertLess('+str(a)+','+str(b)+')');  # Everything OK
        else:
            self.add_result(1, 'assertLess('+str(a)+','+str(b)+')');  # This is not equal

    def assertNone(self, a):
        if a is None:
            self.add_result(0, 'assertNone('+str(a)+')');  # Everything OK
        else:
            self.add_result(1, 'assertNone('+str(a)+')');  # This is not equal

    def add_result(self, r, m):
        currtestr.append((r, m))

def decor_results(r):
    res = []
    for result in r:
        if result[0] == 0:
            res.append('OK')
        else:
            res.append('Failed')
    return res

def r_contains(r, w):
    res = False
    for c in r:
        if c[0] == w:
            res = True
            break
    return res

def test_cases(a):
    tests_run = 0
    ok = True
    if isinstance(a, TestCase) or issubclass(a, TestCase):
        if inspect.isclass(a):
            a = a()
        methods = inspect.getmembers(a, predicate=inspect.ismethod)
        for tmethod in methods:
            if tmethod[0].startswith('test_'):
                tests_run += 1
                getattr(a, tmethod[0])()
                print("Result for " + tmethod[0] + " in " + a.__class__.__name__ + ": " + str(decor_results(currtestr)))
                if r_contains(currtestr, 1):
                    ok = False
                currtestr.clear()
    else:
        raise TypeError
    return (tests_run, ok)

def main():
    # Get testcases
    tests = os.listdir()
    i = 0
    # print(tests)
    while i < len(tests):
        if not tests[i].startswith('test_'):
            tests.remove(tests[i])
        else:
            i+=1
    # print(tests)
    modules = []
    for testf in tests:
        modules.append(importlib.import_module(inspect.getmodulename(testf)))
    # print(modules)
    testcases = []
    for module in modules:
        for testcase in inspect.getmembers(module, predicate=inspect.isclass):
            testcases.append(testcase[1])

    # Run testcases
    testcases_run = 0
    tests_run = 0
    succeded = True
    for testcase in testcases:
        testcases_run += 1
        t = test_cases(testcase)
        tests_run += t[0]
        if t[1] == False:
            succeded = False
            break
    tstr = 'tests'
    if tests_run == 1:
        tstr = 'test'
    tcstr = 'testcases'
    if testcases_run == 1:
        tcstr = 'testcase'
    print('Ran ' + str(tests_run) + ' ' + tstr + ' in ' + str(testcases_run), tcstr)
    if succeded:
        print('OK')
    else:
        print('Failed')

if __name__ == '__main__':
    main()
