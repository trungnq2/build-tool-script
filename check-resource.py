
from termcolor import colored
import json, requests
import os
import sys
from common import check_url, resource_suffixs, url_with_path

real_url = 'https://zalopay.com.vn/v001/tpe/getinsideappresource'
stg_url = 'https://stg.zalopay.com.vn/v001/tpe/getinsideappresource'
sandbox_url = 'https://sandbox.zalopay.com.vn/v001/tpe/getinsideappresource'

app_version = input("Version: ")
valid_versions = {}


def load_app_data(path):
  with open(path, 'rt') as fin:
    content = fin.read()
    data = json.loads(content)

  global valid_versions
  for entry in data['apps']:
    valid_versions[entry['appid']] = entry


def check_url(url):
  r = requests.head(url)
  if r.status_code != 200:
    return (False, "URL %s has problem on server, HTTP code: %d" % (url, r.status_code))

  return (True, "")

def checkResource(app):
  app_id = app['appid']
  image_zip = os.path.basename(app['imageurl'])
  js_zip = os.path.basename(app['jsurl'])
  expected_appinfo = valid_versions.get(app_id, None)
  if 'iconname' in expected_appinfo: 
    actual_icon = app['iconname']
    checkMismatch(app_id, expected_appinfo['iconname'], actual_icon)
  if 'zip' in expected_appinfo: 
    checkMismatch(app_id, expected_appinfo['zip'], image_zip)
    checkMismatch(app_id, expected_appinfo['zip'], js_zip)
  if 'image' in expected_appinfo: 
    checkMismatch(app_id, expected_appinfo['image'], image_zip)
  if 'js' in expected_appinfo: 
    checkMismatch(app_id, expected_appinfo['js'], js_zip)
  if 'ios' in expected_appinfo: 
    checkMismatch(app_id, expected_appinfo['ios'], image_zip)
    checkMismatch(app_id, expected_appinfo['ios'], js_zip)
  if 'android' in expected_appinfo: 
    checkMismatch(app_id, expected_appinfo['android'], image_zip)
    checkMismatch(app_id, expected_appinfo['android'], js_zip)

def checkMismatch(app_id, expected, actual):
  if expected != actual:
    printError("Version mismatch for app %d. Expected [%s], Actual [%s]" % (app_id, expected, actual))

def printError(message):
  print(colored('INVALID with message: %s' % message, 'red'))

def requestResource(dscreen_type, plat_form):
  params = dict(
    appversion = app_version,
    dscreentype = dscreen_type,
    platformcode = plat_form,
    appid = 1,
  )
  resp = requests.get(url=url, params=params)
  data = resp.json()
  if data['returncode'] != 1:
    return (False, "Server return error %d" % data['returncode'])

  resource_list = data['resourcelist']
  if not resource_list or len(resource_list) == 0:
    return (False, 'Empty resource : %s' % dscreen_type)

  base_url = data['baseurl']
  
  for app in resource_list:
    app_id = app['appid']
    if app['apptype'] == 2:
      print(colored('Skip webapp %d' % app_id, 'grey'))
      continue

    image_zip = os.path.basename(app['imageurl'])
    js_zip = os.path.basename(app['jsurl'])

    expected_appinfo = valid_versions.get(app_id, None)
    if expected_appinfo is None:
      print(colored('Skip app %d' % app_id, 'grey'))
      continue
    checkResource(app)


    (result, message) = check_url('%s%s' % (base_url, app['jsurl']))
    if not result:
      printError(message)
      # return (result, message)

    (result, message) = check_url('%s%s' % (base_url, app['imageurl']))
    if not result:
      printError(message)
      # return (result, message)

  return (True, "")

load_app_data('app_data.json')

url = url_with_path('/v001/tpe/getinsideappresource')

for (screen_type, ostype) in resource_suffixs():
  print('Checking for screen type %s on %s ...' % (screen_type, ostype))
  (result, message) = requestResource(screen_type, ostype)
  # if result:
  #   print(colored('VALID', 'green'))
  # else:
  #   print(colored('INVALID with message: %s' % message, 'red'))

