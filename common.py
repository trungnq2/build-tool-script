import json, requests
from pick import pick
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

def yes_no(answer):
  yes = set(['yes','y', 'ye', ''])
  no = set(['no','n'])
     
  while True:
    choice = input(answer).lower()
    if choice in yes:
      return True
    elif choice in no:
      return False
    else:
      print ("Please respond with 'yes' or 'no'\n")

def check_url(url):
  r = requests.head(url)
  if r.status_code != 200:
    return (False, "URL %s has problem on server, HTTP code: %d" % (url, r.status_code))

  return (True, "")

def resource_suffixs():
  return [
    ('hdpi', 'android'),
    ('xhdpi', 'android'),
    ('xxhdpi', 'android'),
    ('ipad1x', 'ios'),
    ('ipad2x', 'ios'),
    ('iphone1x', 'ios'),
    ('iphone2x', 'ios'),
    ('iphone3x', 'ios')
  ]
def choose_environment():
  options = ['Sandbox', 'Staging', 'Real']
  option, index = pick(options, 'Please choose environment: ')
  return option
def url_with_path(path):
  real_url = 'https://zalopay.com.vn'
  stg_url = 'https://stg.zalopay.com.vn'
  sandbox_url = 'https://sandbox.zalopay.com.vn'
  option = choose_environment()
  if option == 'Real':
    base_url = real_url
  elif option == 'Staging':
    base_url = stg_url
  else:
    base_url = sandbox_url
  return urljoin(base_url, path)
def choose_multi_environment():
  title = 'Please choose environment (press SPACE to mark, ENTER to continue): '
  options = ['Internal', 'Sandbox', 'Staging', 'Real']
  selected = pick(options, title, multi_select=True, min_selection_count=1)
  for option, index in selected:
    print (option)
  # print (selected)
