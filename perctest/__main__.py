import inspect, os, importlib, re, perctest, sys
currtestr = []

class TestCase:
    def assertEquals(self, a, b):
        lineno = inspect.currentframe().f_back.f_lineno
        if a == b:
            self.add_result(0, lineno);  # Everything OK
        else:
            self.add_result(1, lineno);  # This is not equal

    def assertSame(self, a, b):
        lineno = inspect.currentframe().f_back.f_lineno
        if a is b:
            self.add_result(0, lineno);  # Everything OK
        else:
            self.add_result(1, lineno);  # This is not equal

    def assertMore(self, a, b):
        lineno = inspect.currentframe().f_back.f_lineno
        if a > b:
            self.add_result(0, lineno);  # Everything OK
        else:
            self.add_result(1, lineno);  # This is not equal

    def assertLess(self, a, b):
        lineno = inspect.currentframe().f_back.f_lineno
        if a < b:
            self.add_result(0, lineno);  # Everything OK
        else:
            self.add_result(1, lineno);  # This is not equal

    def assertNone(self, a):
        lineno = inspect.currentframe().f_back.f_lineno
        if a is None:
            self.add_result(0, lineno);  # Everything OK
        else:
            self.add_result(1, lineno);  # This is not equal

    def add_result(self, r, ln):
        #print('Appending', (r,ln))
        perctest.__main__.currtestr.append((r, ln))
        #print(currtestr)

def decor_results(r):
    res = []
    for result in r:
        if result[0] == 0:
            res.append('OK')
        else:
            res.append('Failed')
    return res

def get_lines_around(filename, lineno):
    flines = open(filename, mode='r').readlines()
    padding = 5
    lcolor = '\033[33m'
    red = '\033[1;31m'
    reset = '\033[0m'
    # Decorate it
    r0 = ''
    r1 = ' '*(padding-len('>' + str(lineno)))+red+'>'+str(lineno)+('|'+flines[lineno-1]+reset)
    r2 = ''
    if lineno < len(flines) and lineno == 1:
        r2 = ' '*(padding-len(str(lineno+1)))+lcolor+str(lineno+1)+('|'+reset+flines[lineno])
    elif lineno == len(flines) and lineno > 1:
        r0 = ' '*(padding-len(str(lineno-1)))+lcolor+str(lineno-1)+('|'+reset+flines[lineno-2])
    else:
        r2 = ' '*(padding-len(str(lineno+1)))+lcolor+str(lineno+1)+('|'+reset+flines[lineno])
        r0 = ' '*(padding-len(str(lineno-1)))+lcolor+str(lineno-1)+('|'+reset+flines[lineno-2])
    return r0 + r1 + r2

def r_contains(r, w):
    res = False
    for c in r:
        if c[0] == w:
            res = True
            break
    return res

def removentests(l, f=True):
    i = 0
    while i < len(l):
        if f:
            if not l[i].startswith('test_'):
                l.remove(l[i])
            else:
                i+=1
        else:
            if not l[i][0].startswith('test_'):
                l.remove(l[i])
            else:
                i+=1
    return l

def test_cases(a):
    test_caser = []
    tests_run = 0
    ok = True
    if isinstance(a, TestCase) or issubclass(a, perctest.__main__.TestCase):
        if inspect.isclass(a):
            a = a()
        methods = inspect.getmembers(a, predicate=inspect.ismethod)
        for tmethod in methods:
            if tmethod[0].startswith('test_'):
                tests_run += 1
                tfunc = getattr(a, tmethod[0])
                #print(tfunc)
                tfunc()
                #print("Result for " + tmethod[0] + " in " + a.__class__.__name__ + ": " + str(decor_results(perctest.__main__.currtestr)))
                test_caser.append(perctest.__main__.currtestr.copy())
                if r_contains(perctest.__main__.currtestr, 1):
                    ok = False
                #print(perctest.__main__.currtestr)
                perctest.__main__.currtestr = []
    else:
        raise TypeError(inspect.getmro(a), TestCase, perctest.__main__.TestCase)
    return (tests_run, ok, test_caser)

def main():
    # Get testcases
    tests = os.listdir()
    i = 0
    # print(tests)
    # while i < len(tests):
    #     if not tests[i].startswith('test_'):
    #         tests.remove(tests[i])
    #     else:
    #         i+=1
    tests = removentests(tests)
    # print(tests)
    modules = []
    #print(os.getcwd())
    sys.path.insert(0,os.getcwd())
    for testf in tests:
        #print(testf)
        modules.append(importlib.import_module(inspect.getmodulename(testf)))
    # print(modules)
    testcases = []
    for module in modules:
        for testcase in inspect.getmembers(module, predicate=inspect.isclass):
            testcases.append(testcase[1])

    # Run testcases
    testcases_run = 0
    testcasesr = []
    tests_run = 0
    succeded = True
    for testcase in testcases:
        testcases_run += 1
        t = test_cases(testcase)
        fname = inspect.getfile(testcase)
        for test in t[2]:
            for assertion in test:
                failed = assertion[0] == 1
                lineno = assertion[1]
                if failed:
                    methodtests = removentests(inspect.getmembers(testcase(), predicate=inspect.ismethod), f=False)
                    method = methodtests[t[2].index(test)]
                    #print(method)
                    print('')
                    print('\033[0m\033[1;30;41mFailed @ def', method[0]+'()', 'in class', testcase.__name__, 'in', fname,'\033[0m')
                    print('')
                    print(get_lines_around(fname, lineno))
        tests_run += t[0]
        testcasesr.append(t[2])
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
        print('')
        print('         \033[0m\033[1;30;42m                          \033[0m')
        print('         \033[0m\033[1;30;42m            OK            \033[0m')
        print('         \033[0m\033[1;30;42m                          \033[0m')
        print('')
    else:
        print('')
        print('         \033[0m\033[1;30;41m                          \033[0m')
        print('         \033[0m\033[1;30;41m          Failed          \033[0m')
        print('         \033[0m\033[1;30;41m                          \033[0m')
        print('')

if __name__ == '__main__':
    main()
