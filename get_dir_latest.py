import os
import re

#get all subdirs
def all_subdirs_of(dir_loc='.'):
  result = []

  for d in os.listdir(dir_loc):
    bd = os.path.join(dir_loc, d)

    #appending parent dir to subdirs
    if os.path.isdir(bd): 
            result.append(bd)

  return result

#gets latest dir
def get_latest_dir(all_dirs):

  #return path of latest dir
  latest_subdir = max(all_dirs, key=os.path.getmtime)
  return latest_subdir

#get particular file
def get_loc_file(file_dir_loc, regex_string):
  prog = re.compile(regex_string.strip().lower())
  #not case sensitive
  
  all_files = os.listdir(file_dir_loc)
  for file in all_files:

    if prog.match(file.lower()):
      return file

  return False

#find phrase starting from bottom of the file
def find_in_file(file, phrase):
  #not case sensitive
  status = False

  phrase = re.compile(phrase.strip().lower())

  with open(file, 'r') as textfile:
    lines = textfile.readlines()

    for line in reversed(lines):

      if phrase.match(line.strip().lower()):
        status = True
        break
 
  return status
all_subdirs = all_subdirs_of(r'C:\Users\aldri\OneDrive\Desktop\AutonomousCar')

latest_dir = get_latest_dir(all_subdirs)
print(get_loc_file(lak, 'application'))
