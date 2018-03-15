import json
import os
import shutil
import subprocess
import glob
from os import listdir, path
from os.path import isfile, join

import zpzip
import resource

import sys

svn_dir = '/Users/mrbu/Desktop/VNG/SVN_Resource/zalopay-sdk'
root_app = os.getcwd()

def build_app(sandbox, staging, zip_name): 

  root_app = os.getcwd()
  buildFolderName =zip_name.replace('.zip','')
  print(os.getcwd())
  d = "./output/%s/ios" %buildFolderName
  os.chdir(d)
  
  ios_sortout_resources(zip_name)
  os.chdir('../android')
  android_sortout_resources(zip_name)
  #copyToSvn(sandbox, staging, zip_name, root_app)

def copyToSvn(sandbox, staging, zip_name, root_app):
  copy_resource_tosvn(zip_name, root_app, sandbox, staging)
  copy_js_tosvn(zip_name, root_app, sandbox, staging)
  return

#iOS
def ios_sortout_resources(zip_name):
  root_src_dir = './assets'

  images_dict = resource.ios_map_images(root_src_dir)

  root_target_dir1x = "./1x/assets"
  root_target_dir2x = "./2x/assets"
  root_target_dir3x = "./3x/assets"

  os.system('rm -rf 1x 2x 3x')
  #os.system("mkdir %s %s %s" %(root_target_dir1x, root_target_dir2x, root_target_dir3x))
  os.system('mkdir -p '+ root_target_dir1x + ' ' +root_target_dir2x + ' ' + root_target_dir3x)

  resource.clone_folder_structure('./assets', root_target_dir1x)
  resource.clone_folder_structure('./assets', root_target_dir2x)
  resource.clone_folder_structure('./assets', root_target_dir3x)

  resource.ios_copy_resource_scale('./1x', images_dict, 2)
  resource.ios_copy_resource_scale('./2x', images_dict, 2)
  resource.ios_copy_resource_scale('./3x', images_dict, 3)
  if path.exists('zips'):
    shutil.rmtree('zips')
  os.makedirs('zips/js')
  os.makedirs('zips/images/iphone1x')
  os.makedirs('zips/images/iphone2x')
  os.makedirs('zips/images/iphone3x')

  zip_dir = join('./zips/js', zip_name)
  if path.exists('fonts'):
    os.system('zip -r %s main.jsbundle fonts' %(zip_dir ))
  else:
    os.system('zip -r %s main.jsbundle' %(zip_dir ))

  os.chdir('./1x')
  zpzip.zip_folder('./assets', os.path.join('../zips/images/iphone1x/', zip_name))
  os.chdir('../2x')
  zpzip.zip_folder('./assets', os.path.join('../zips/images/iphone2x/', zip_name))
  os.chdir('../3x')
  zpzip.zip_folder('./assets', os.path.join('../zips/images/iphone3x/', zip_name))
  os.chdir('..')

def android_sortout_resources(zip_name):
  resource.copy_resource_android()
  if path.exists('zips'):
    shutil.rmtree('zips')
  os.makedirs('zips')
  os.makedirs('zips/hdpi')
  os.makedirs('zips/xhdpi')
  os.makedirs('zips/xxhdpi')
  os.makedirs('zips/js')

  zip_dir = join('./zips/js', zip_name)
  if path.exists('fonts'):
    os.system('zip -r %s main.jsbundle fonts' %(zip_dir ))
  else:
    os.system('zip -r %s main.jsbundle' %(zip_dir ))

  # zpzip.zip_folder('./drawable-hdpi', os.path.join('./zips/hdpi/', zip_name))
  # zpzip.zip_folder('./drawable-xhdpi', os.path.join('./zips/xhdpi/', zip_name))
  # zpzip.zip_folder('./drawable-xxhdpi', os.path.join('./zips/xxhdpi/', zip_name))

  os.system('zip -r zips/hdpi/%s drawable-*' %zip_name)
  os.system('zip -r zips/xhdpi/%s drawable-*' %zip_name)
  os.system('zip -r zips/xxhdpi/%s drawable-*'%zip_name)
  
def copy_js_tosvn(zip_name, root_app, sandbox, staging):
  # os.chdir(root_app)
  # os.chdir('./output/ios') 
  
  # ios_src_dir = join('.\\zips\\js', zip_name)
  
  # if sandbox:
  #   ios_target_dir = join(svn_dir, 'sandbox/ps_res/ios/js')
  #   shutil.copy(ios_src_dir, ios_target_dir)
  # if staging:
  #   ios_target_dir = join(svn_dir, 'staging/ps_res/ios/js')
  #   shutil.copy(ios_src_dir, ios_target_dir)
  
  # os.chdir('../android')
  # android_src_dir = join('.\\zips\\js', zip_name)
  
  # if sandbox:
  #   android_target_dir = join(svn_dir, 'sandbox/ps_res/android/js')
  #   shutil.copy(android_src_dir, android_target_dir)
  # if staging:
  #   android_target_dir = join(svn_dir, 'staging/ps_res/android/js')
  #   shutil.copy(android_src_dir, android_target_dir)
  return
    

def copy_resource_tosvn(zip_name, root_app, sandbox, staging):
  android_suffixs = [
    'hdpi',
    'xhdpi',
    'xxhdpi'
  ]
  ios_suffixs = [
    'ipad1x',
    'ipad2x',
    'ipad3x',
    'iphone1x',
    'iphone2x',
    'iphone3x',
  ]
  os.chdir(root_app)
  os.chdir('./output/android') 

  for suffix in android_suffixs:
    svn_src_dir = join(join('./zips', suffix), '*')
    if sandbox:
      svn_target_dir = join(join(svn_dir, 'sandbox/ps_res/android/images'), suffix)
      os.system('cp -r %s %s'%(svn_src_dir, svn_target_dir))
      
    if staging:
      svn_target_dir = join(join(svn_dir, 'staging/ps_res/android/images'), suffix)
      os.system('cp -r %s %s'%(svn_src_dir, svn_target_dir))
  os.chdir('../ios')

  for suffix in ios_suffixs:
    svn_src_dir = join('./zips/images', join(suffix.replace('ipad','iphone'), zip_name))
    print (svn_src_dir)
    if sandbox:
      svn_target_dir = join(join(svn_dir, 'sandbox/ps_res/ios/images'), suffix)
      os.system('cp -r %s %s'%(svn_src_dir, svn_target_dir))
    if staging:
      svn_target_dir = join(join(svn_dir, 'staging/ps_res/ios/images'), suffix)
      os.system('cp -r %s %s'%(svn_src_dir, svn_target_dir))
