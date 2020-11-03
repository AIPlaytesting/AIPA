import pkgutil
import sys, inspect
import os
import importlib

def load_all_modules_from_dir(filename):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    dirname = cur_dir + '\\'+filename
    print("dir: ", dirname)
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        print("package name",package_name)
        print("full pack name",full_package_name)
        mname = '.'+filename+'.'+package_name
        print('module name',mname)
        m = importlib.import_module(mname,package= 'gameplay_extension')
        print_classes(m)
        # if full_package_name not in sys.modules:
        #     module = importer.find_module(package_name).load_module(full_package_name)
        #     print (module)
def print_classes(module):
    print(sys.modules.keys())
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            print(obj)

#load_all_modules_from_dir('buffs')
m = importlib.import_module('buffs.strength')
print(m)