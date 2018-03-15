import os
import shutil
from os import listdir, path


def clone_folder_structure(root_src_dir, root_target_dir):
  for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_target_dir)
    #dst_dir = os.getcwd() + dst_dir.replace('.','').replace('/','\\')
    print('Currnet dir: ', os.getcwd())
    print("dest: ", dst_dir)

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)


def ios_find_max_scale(scale_dict, scale):
  for x in range(scale, 0, -1):
    if x in scale_dict:
      return scale_dict[x]
  return None


def ios_copy_resource_scale(root_target_dir, images_dict, scale):
  for (key, resource) in images_dict.items():
    path = ios_find_max_scale(resource, scale)
    print("resource for scale %d: %s" % (scale, path))

    if path is None:
      print("cannot find resource %s for scale %d" % (key, scale))
    src_file = path
    dst_dir =  os.path.join(root_target_dir, path)
    print("Copy to %s" % dst_dir)
    shutil.copy(src_file, dst_dir)


def ios_get_scale_and_basename(file_name):
  import re
  pattern = "(.*)(@(\d|\d\.\d)x)(.*)"
  matches = re.compile(pattern, 0).match(file_name)
  if matches is None:
    return (1, file_name)

  return_value = ((float)(matches.group(3)), "".join([matches.group(1), matches.group(4)]))
  return return_value


def ios_map_images(root_src_dir):
  images_dict = {}
  for src_dir, dirs, files in os.walk(root_src_dir):
    for file_ in files:
      src_file = os.path.join(src_dir, file_)
      (scale, basename) = ios_get_scale_and_basename(file_)
      src_basename = os.path.join(src_dir, basename)
      if src_basename not in images_dict:
        images_dict[src_basename] = {}
      images_dict[src_basename][scale] = src_file

  return images_dict



def android_find_max_scale(scale_dict, scale):
  scale_ranges = ["xxxhdpi", "xxhdpi", "xhdpi", "hdpi", "mdpi"]
  s_index = scale_ranges.index(scale)
  for_range = scale_ranges[s_index:]
  print(for_range)
  for x in for_range:
    if x in scale_dict:
      return scale_dict[x]
  return None


def android_copy_resource_scale(root_target_dir, images_dict, scale):  
  for (key, resource) in images_dict.items():
    path = android_find_max_scale(resource, scale)
    print("resource for scale %s: %s" % (scale, path))

    if path is None:
      print("cannot find resource %s for scale %s" % (key, scale))
    src_file = path
    dst_dir = os.path.join(root_target_dir, path)
    print("Copy to %s" % dst_dir)
    shutil.copy(src_file, dst_dir)


def android_map_images(root_src_dir):
  images_dict = {}
  for src_dir, dirs, files in os.walk(root_src_dir):
    print("dir: %s" % src_dir)
    scale = ""
    if src_dir.startswith("%s/drawable-" % root_src_dir):
      scale = src_dir.replace("%s/drawable-" % root_src_dir, "")
      print("drawable-%s" % scale)
    else:
      continue
    for file_ in files:
      src_file = os.path.join(src_dir, file_)
      print("walk file: %s: fileName: %s" % (src_file, file_))
      src_basename = file_
      if src_basename not in images_dict:
        images_dict[src_basename] = {}
      images_dict[src_basename][scale] = src_file

  print("result: %r" % images_dict)
  return images_dict
def copy_resource_android():
  copy_notreplace('drawable-mdpi', 'drawable-hdpi')
  copy_notreplace('drawable-hdpi', 'drawable-xhdpi')
  copy_notreplace('drawable-xhdpi', 'drawable-xxhdpi')

def copy_notreplace(src_dir, target_dir):
  if os.path.exists(src_dir) and os.path.exists(target_dir):
    for file_ in os.listdir(src_dir):
      src_file = os.path.join(src_dir, file_)
      dst_file = os.path.join(target_dir, file_)
      if not os.path.exists(dst_file):
        shutil.copy(src_file, dst_file)
        