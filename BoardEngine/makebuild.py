import json
import sys
import os
import shutil
from distutils.dir_util import copy_tree

ORIGINAL_BUILD_DIR = 'out'

def load_json_from_file(file_path):
    with open(file_path, "r") as file:
        raw_json_data = file.read()
        return json.loads(raw_json_data)  

def save_json_obj_to_file(obj,path):
    json_str = json.dumps(obj, indent = 4)
    f= open(path,"w+")
    f.write(json_str)
    f.close()

def makesure_clean_path(dest_path):
    if os.path.exists(dest_path):
        print('[build]-clean the path: '+dest_path)
        shutil.rmtree(dest_path)
    os.makedirs(dest_path)

def copy_dir(src,dest):
    print("[build]- copy",src,"to",dest)
    copy_tree(src,dest)

def build(root_path):
    # copy orginal build
    print("[build]- copy source build files ...")
    config = load_json_from_file(root_path+'\\BoardEngine-win32-x64\\resources\\app\\config.json')
    print("[build]- config: ",config)
    output_dir = config['buildConfig']['outputDir']
    makesure_clean_path(output_dir)
    copy_tree(root_path,output_dir)

    # define paths
    res_path = output_dir+'\\BoardEngine-win32-x64\\resources\\app'
    executables_path = res_path+'\\executables'

    # save new config.json
    print("[build] - make config.json...")
    config['isDevMode'] = False
    save_json_obj_to_file(config,res_path+'\\config.json')

    #copy pyproj
    print("[build] - make python project source codes...")
    pyproj_dir = executables_path +'\\pyproj'
    makesure_clean_path(pyproj_dir)
    copy_dir(config['devDependencies']['pythonProject'],pyproj_dir)
    
    # redirect python launcher of Unity
    print("[build] - unity python launcher...")
    unityPyLuancherSrc = config['buildConfig']['unityPythonLauncherSource']
    unityPyLuancherDest = executables_path +'\\unitybuild\\AIPA_Data\\backend.bat'
    if os.path.exists(unityPyLuancherDest):
        os.remove(unityPyLuancherDest)
    shutil.copyfile(unityPyLuancherSrc , unityPyLuancherDest)

    #build pyexe(standardOps not working...)
    print("[build] - make python environment...")
    pyexe_dir = executables_path +'\\pyexe'
    makesure_clean_path(pyexe_dir)
    copy_dir(config['buildConfig']['pythonEnvSource'],pyexe_dir)

    print("[build] - done")   

build(ORIGINAL_BUILD_DIR)