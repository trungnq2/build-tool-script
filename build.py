from pick import pick
from os import walk
import os
from os.path import join
from buildoneapp import build_app, copyToSvn
import sys
import json
import shutil
import time
from common import yes_no
import result
import subprocess
import shutil

def load_build_file():
  with open('./build.json') as data_file:    
     return json.loads(data_file.read())['apps']

def get_app_version(jsonFile):
    with open(jsonFile) as data_file:    
      return json.loads(data_file.read())['version']

def git_commit(absolute_path, files, message):
    print("Current D: ", os.getcwd())
    print("Commiting: ", absolute_path, files, message)
    subprocess.call(["git", "add"] + files)
    subprocess.call(["git", "commit", "-m", message])
    # os.system("git add ", files)
    return

def choose_files_commit(path):
  options = []
  for item in os.listdir(path):
    options.append(item)
  title= "Choose Item To Commit"
  selected = pick(options, title, multi_select = True, min_selection_count=1)
  files = []
  for f, index in selected:
    files.append(f)
  return files

def choose_app():
  options = []
  for f in apps_info:
      options.append(f['name'])
  title = 'Please choose apps (press SPACE to mark, ENTER to continue): '
  selected = pick(options, title, multi_select=True, min_selection_count=1)
  return selected

def choose_updateOption(selectedApps):
  options=['None', 'All Apps']
  for app_name, index in selectedApps:
    options.append(app_name)
  title = 'Please choose app to run yarn upgrade'
  selected = pick(options,title)

  if selected[0] == u"All Apps":
    return selectedApps
  if selected[0] == u"None":
    return
  return [selected]

def input_versions():
  versions = []
  print('Input Versions, press [n]ext to proceed')
  while True:
    version = input('Enter a version: ')  
    if version == 'n':
      break  
    versions.insert(0,version)

  build = input('Build ? [y]es | [n]o: ')
  if build == 'y':
    return versions
  else:
    return

# def initAppJson_deprecated(version, apps):
  appJson  = []
  for app_name,index in apps:
    app = apps_info[index]
    app_id = app['appid']
    copyOnly = False
    print('>>>>> APP: %s|appid: %s' %(app_name, app_id))

    if 'copyonly' in app:
      copyOnly = app['copyonly']

    zip_name = ''

    if not copyOnly:
      build_number = input("Build number: ")
      zip_name = "%s.%s.%s_%s.zip" %(str(app_id).zfill(3), version, time.strftime("%Y%m%d"), build_number.zfill(3))
    else:
      if 'zip' in app:
        zip_name = app['zip']
    print (zip_name)
    if zip_name == '':
      print('Skip APP: %s|appid: %s' %(app_name, app_id))
      continue
    app_info = {
      key:app[key] for key in app
    }
    app_info['zip'] = zip_name
    app_info['copyonly'] = copyOnly

    appJson.append(app_info)
  return appJson

def init_app_info(version, app):
  app_id = app['appid']
  copyOnly = False
  print('>>>>> APP: %s|appid: %s' %(app_name, app_id))

  if 'copyonly' in app:
    copyOnly = app['copyonly']

  zip_name = ''

  if not copyOnly:
    build_number = input("Build number: ")
    zip_name = "%s.%s.%s_%s.zip" %(str(app_id).zfill(3), version, time.strftime("%Y%m%d"), build_number.zfill(3))
  else:
    if 'zip' in app:
      zip_name = app['zip']
  print (zip_name)
  # if zip_name == '':
  #   print('Skip APP: %s|appid: %s' %(app_name, app_id))
  #   continue
  app_info = {
    key:app[key] for key in app
  }
  app_info['zip'] = zip_name
  app_info['copyonly'] = copyOnly
  app_info['version'] = version

  print("APP INFO: ", app_info)
  return app_info

def get_app_path(name):
  for app in apps_info:
    if app['name'] == name:
      return app['path']
  return

def init_app_build(app):
  #change working directory
  os.chdir(root_dir)

  app_id = app['appid']
  zip_name = app['zip']
  app_dir = app['path']
  copyOnly = app['copyonly']
  app.pop('copyonly', 0)
  app.pop('path', 0)
  print('>>>>> BUILD APP: |name: %s|id: %s|%s' %(zip_name,app_id, app_dir))

  os.chdir(app_dir)
  if not copyOnly:
    build_react_native_dir = join(root_dir, 'script/build-react-native.sh')

    print("APPP VERSION %s" %app['version'])

    #command = build_react_native_dir.replace('\\', '/') + " " + app['zip'].replace('.zip', '')
    arg = app['zip'].replace('.zip', '')
    command = "bash %s %s" %(build_react_native_dir, str(arg))
    print("Command %s" %command)
    os.system(command)
    #os.system(command)
    #"%s %s" %(build_react_native_dir.replace('\\', '/'), app['version'])
    build_app(sandbox, staging, zip_name)
  else: 
    root_app = os.getcwd()
    print('root_app: ', root_app)
    copyToSvn(sandbox, staging, zip_name, root_app)


def getAppsVersions(apps):
  vers = ''
  for app in apps:
    try:
      jsonFile = "%s/%s" %(app['path'], "package.json")
      ver = get_app_version(jsonFile)
      vers= vers + "\n>>>>%s : %s" %(app['name'], ver)
    except:
      pass
  return vers

apps_info = load_build_file()

os.chdir('../')
root_dir = os.getcwd()
apps = choose_app()
appsToUpdate = choose_updateOption(apps)

print(getAppsVersions(apps_info))

sandbox = False
staging = False
for param in sys.argv:
  if param == 'sandbox':
    sandbox = True
  if param == 'staging':
    staging = True
if not (sandbox or staging):
  exit()

environment = ''
print ('>>> Environment: ')
if sandbox:
  environment = "Sandbox"
  print ('>>> SANDBOX')
if staging:
  environment = "Staging"
  print ('>>> STAGING')

versions = input_versions()

# No use ?!
resultJson = []

result = []

if appsToUpdate != None:
  for name, i in appsToUpdate:
      os.chdir(get_app_path(name))
      print("Upgrading %s" %name)
      os.system("(yarn upgrade || (yarn install && yarn upgrade)) > UpdateLog.txt")
      os.system('cls')
      print("Finished upgrading %s. See UpdateLog.txt for more detail" %name)
else:
  print("Skipped Yarn Upgrade")

for app_name,index in apps:
    os.chdir(root_dir)
    app_info = apps_info[index]
    app_dir = app_info['path']

    os.chdir(app_dir)

    shutil.rmtree('./output', ignore_errors = True)
    os.system('cls')
    print("Current working folder is %s" %(os.getcwd()))
   
    for version in versions:

      # #Commit to local
      # files = choose_files_commit(os.getcwd())
      # #[App-${appid}][${Environment}] Bump version ${version}
      # message = "[App-%s][%s] Bump version %s" %(app_info['appid'], environment, version)
      # git_commit(app_dir, files, message)

      print("------Building %s Version %s ------" %(app_name, version))
      app = init_app_info(version, app_info)
      init_app_build(app)
      #revert back to the top folder
      os.chdir(root_dir)
      os.chdir(app_dir)

os.chdir(root_dir)
os.chdir('./script')
