import operator
import subprocess
import sys
import os
from functools import reduce

# Make a list into a space seperated string
def list_2_string(text_list):
  return reduce(operator.add, [t+" " for t in text_list])

# Execute a command without generating a new shell
def execute_noshell(command, echo=True):
  if echo:
    print("   ", list_2_string(command))
    sys.stdout.flush()

  #print(" ".join(command))
  #import stat
  #st = os.stat(command[0])
  #print(oct(st.st_mode))
  #os.chmod(command[0], st.st_mode | stat.S_IEXEC)
  if subprocess.call(command, shell=False) != 0:
    sys.stderr.write("  Failure...\n")
    return 1
  return 0

# Execute a command within a new shell
def execute_shell(command, echo=True):
  if echo:
    if isinstance(command, list):
      print("   ", command[0])
    else:
      print("   ", command)
    sys.stdout.flush()

  if subprocess.call(command, shell=True) != 0:
    sys.stderr.write("  Failure...\n")
    return 1
  return 0

# Execute a command without generating a new shell
# and return any output from "stdout"
def stdout_noshell(command, echo=True):
  if echo:
    print("   ", list_2_string(command))
    sys.stdout.flush()

  sub_p = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
  output = sub_p.communicate()[0]
  status = sub_p.returncode
  if status != 0:
    sys.stderr.write("  Failure...\n")
    return (1, "Failure")
  return (0, output)

# Execute a command within a new shell
# and return any output from "stdout"
def stdout_shell(command, echo=True):
  if echo:
    if isinstance(command, list):
      print("   ", command[0])
    else:
      print("   ", command)
    sys.stdout.flush()

  sub_p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  output = sub_p.communicate()[0]
  status = sub_p.returncode
  if status != 0:
    sys.stderr.write("  Failure...\n")
    return (1, "Failure")
  return (0, output)

# Return a list of integers after parsing a string of integers, commas, and
# dashes:  # specifies an integer and #-# specifies an integer range.  An
# number of these integers and integer ranges can be specified as part of a
# comma seperated list.  For example,
#
#     2          -> [2]
#     1,2,4,8    -> [1,2,4,8]
#     1-2,4,8-16 -> [1,2,4,8,9,10,11,12,13,14,15,16]
#
def parse_int_list(input_list):
  retlist = []

  elems = input_list.replace(" ", "").replace("\t", "").split(",")
  for elem in elems:
    minmax = elem.split("-")
    if len(minmax) == 1:
      retlist.append(int(minmax[0]))
    else:
      for i in range(int(minmax[0]), int(minmax[1])+1):
        retlist.append(i)

  return sorted(list(set(retlist)))

# Return a dictionary of integers from a string
# Can be used in forming key:value pairs for GPU blocks:threads,
# OpenCL global:local, etc.
# E.g:
# 2:3      -> {2:3}
# 2:3,4:5  -> {2:3, 4:5}
#
def parse_int_dict(string):
  retdict = dict((int(x.strip()), int(y.strip()))
    for x, y in (element.split(':') for element in string.split(',')))

  return retdict

# Make a new directory if it doesn't already exist
def make_dir_if_needed(input_dir, name, echo=True):
  if not os.path.exists(input_dir):
    command = ["/bin/mkdir", input_dir]
    if execute_noshell(command, echo) != 0:
      sys.stderr.write("Unable to make %s directory, %s\n" % (name, input_dir))
  else:
    return False

  return True
