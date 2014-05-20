import io
import ast
import re
import inspect
import importlib.machinery
import os.path

def find_lines(lines, pattern=''):
    strings = list(filter(lambda l: pattern in l,lines))
    return strings

def find_line(lines, pattern=''):
    elem = list(filter(lambda l:pattern in l,lines))
    return elem[0] if len(elem) else None

def print_dumps(lines):
    for l in lines:
        print_dump(l)

def print_dump(line):
    dump = ast.dump(ast.parse(line))
    print("line: %sdump: %s\n" % (line,dump))

def isFunction(obj):
    return hasattr(obj, '__call__')

def verify_function(args, func1, func2):
    equivalent = True
    for arg in args:
        result1 = func1(arg)
        result2 = func2(arg)
        equivalent = equivalent and result1 == result2
        if not equivalent: return equivalent
    return equivalent

def print_result(func_name, result):
    print('Test %s have completed successfully.' % func_name if result else 'Test %s have failed.' % func_name)

def run_tests(tests={},testvars={},module_lines=[]):
    variables = sorted(tests.keys())
    temp_result = False
    for v in variables:
        print('\nTests for variable %s:' % v)
        good_job = True
        testvar = testvars[v]
        for test in tests[v]:            
            testfuncargs = test[0]
            testfunc = test[1]
            
            if(testfunc != None and len(testfuncargs)):
                if(isFunction(testvar)):
                    temp_result = verify_function(testfuncargs,testvar,testfunc)
                    print_result(testfunc.__name__, temp_result)
                    good_job = good_job and temp_result
                elif testfunc.__name__ == 'find_line':
                    for funcarg in testfuncargs:
                        print('%s(\'%s\')\t\t' % (testfunc.__name__,funcarg))
                        temp_result = testfunc(find_lines(module_lines,v),funcarg) != None
                        print_result(testfunc.__name__, temp_result)
                        good_job = good_job and temp_result
                elif len(inspect.getfullargspec(testfunc)[0]) == 2:
                    for funcarg in testfuncargs:
                        temp_result = testfunc(funcarg,testvar)
                        print_result(testfunc.__name__, temp_result)
                        good_job = good_job and temp_result
                else:
                    temp_result = testfunc(testvar)
                    print_result(testfunc.__name__, temp_result)
                    good_job = good_job and temp_result
                
        print('All tests have completed successfully.' if good_job else 'Try next time, please. Fix errors.')
                        
###
#START>>>Section for predefined test functions
###
def e1_testfunction(obj):
    return obj > 10

def e3_testfunction(o1,o2):
    return True if o1 == o2 else None

def e5_testfunction(o1):
    return type(o1) is tuple

def e7_testfunction(a):
    return a * a
###
#END>>>Section for predefined test functions
###
predefined_tests = \
    {'exercise1':[(['%','/'],find_line), ([0],e1_testfunction)],
     'exercise2':[(['ingstr','ing','ingstr'],find_line)],
     'exercise3':[([[1,2,3,4,5]],e3_testfunction)],
     'exercise4':[([],None)],
     'exercise5':[([0],e5_testfunction), (['exercise1','exercise2'],find_line)],
     'exercise6':[(['math','log'],find_line)],
     'exercise7':[([1,2,3,4],e7_testfunction)],
     'exercise8':[([],None)]
     }

def start_app():
    path = input('Enter full path to file with exercises: ')

    if(len(path) and path.endswith('.py') and os.path.exists(path)):
        dynamic_module_lines = list(open(path))
        loader = importlib.machinery.SourceFileLoader('exerci5e5._exerci5e_',path)
        dynamic_loaded_module = loader.load_module('exerci5e5._exerci5e_')
        dynamic_module_vars = vars(dynamic_loaded_module).copy()

        run_tests(predefined_tests, dynamic_module_vars, dynamic_module_lines)
    else:
        print('Check file path and run application again')