import os
import json

def createTxtFromJSON():
  file = open("app_data.txt", "w")

  with open("app_data.json") as app_data:
    json_ = json.load(app_data)
    apps = json_['apps']
    # sortlist = sorted(apps, key=lambda k: k['appid']) 
    for app in apps:
      file.write("App: %s \n"%app['appid'])
      file.write("Name: %s \n"%app['zip'])
      file.write("\n")
  file.write("Version: \n" )
  file.write("Environment: \n")
  file.write("Platform: iOS + Android \n")
  file.close()

def write_output(file_path, data):
  print("Full Path %s" % os.getcwd())

  print("Updating %s" % file_path)
  with open(file_path, 'w') as outfile:
    json.dump(data, outfile, indent=4)

def createAppJSON(data): 
  sortlist = sorted(data, key=lambda k: k['appid'])
  write_output("app_data.json", {"apps": sortlist})