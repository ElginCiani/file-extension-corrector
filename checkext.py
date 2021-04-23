#!/usr/bin/env python3
import os
import optparse
import subprocess
import filetype

options = None

def parse_args():
  parser = optparse.OptionParser(
    """
    This software is provided \"AS IS\", without warranty of any kind.\n
    'checkext' is a tool used to make sure that files really are
    what their extensions say they are.

    run with: '{Python Path} checkext.py [options]'\n\n
    Tool created by: Elgin Ciani
    """,
    version="%prog 1.0")

  #Available command line arguments
  parser.add_option("-t", "--type", dest="type", action="append", type="string", help="File type(s) to check for. Comma delimited (e.g. -t jpg,png). Input * for all.")
  parser.add_option("-c", "--count", dest="count", action="store_true",  default=False, help="Counts the number of files with incorrect extension.")
  parser.add_option("-d", "--delete", dest="delete", action="store_true", default=False, help="Delete file if the extension does not match true file type.")
  parser.add_option("-f", "--fix", dest="fix", action="store_true", default=False, help="Rename file extension if it does not match true file type.")
  parser.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Check files in subdirectories as well.")
  parser.add_option("-R", "--rename", dest="rename", action="append", type="string", help="Renames all extensions from a to b (i.e. -R a,b).")
  parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help="Enable this flag to turn off any print logging.")
  parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Enable this flag for extra logging.")
  
  global options
  (options, arguments) = parser.parse_args()

  #Throw error if user does not specify required parameters
  if not options.type and not options.rename:
    parser.error("[-] Please specify file type(s). Use * to check all. See --help for more info.")
  elif options.rename and (options.delete or options.fix):
    parser.error("[-] Do not set --rename flag along with --delete or --fix.")
  elif options.type and options.rename:
    parser.error("[-] Do not set --type and --rename flags simultaneously.")
  elif options.delete and options.fix:
    parser.error("[-] Do not set --delete and --fix flags simultaneously.")
  elif options.quiet and options.count:
    parser.error("[-] Do not set --quiet and --count flags simultaneously.")
  elif options.quiet and options.verbose:
    parser.error("[-] Do not set --quiet and --verbose flags simultaneously.")
  ## End: Error scenarios ##
  return options

########## MAIN ##########
def main():
  options = parse_args() #Option parser

  #Initialize counters
  count = 0
  num_unknown = 0

  #For renaming all extensions from a to b (i.e. -R a,b)
  if not options.type and options.rename:
    types = options.rename[0].split(",") #Array of specified names
    if options.verbose:
      print("Renaming all extensions of type", types[0], "to", types[1])
    for root, dirs, files in os.walk("."):
      for filename in files:
        filepath = root+"\\"+filename
        split_tup = os.path.splitext(filepath)
        if split_tup[1][1:] == types[0]:
          new_name = split_tup[0]+'.'+types[1]
          if options.verbose:
            print("Renaming", filepath, "to", new_name)
          os.rename(filepath, new_name)
          count += 1
      if options.recursive:
        for dir in dirs:
          if options.verbose:
            print("Checking dir:", dir)
      else: #Prevent descending into subfolders
        break
    if options.count:
      print("Renamed", count, "files.")
    return

  types = options.type[0].split(",") #Array of specified types

  #Check all files
  for root, dirs, files in os.walk("."):
    for filename in files:
      if options.verbose:
        print("Checking file:", filename)
      filepath = root+"\\"+filename
      kind = filetype.guess(filepath)
      if kind is None:
        print('Cannot guess file type!')
        continue
      else:
        if options.verbose:
          print('File extension: %s' % kind.extension)
          print('File MIME type: %s' % kind.mime)
        if '*' in types or kind.extension in types:
          split_tup = os.path.splitext(filepath)
          if kind.extension != split_tup[1][1:].lower(): #File extension is wrong
            if options.verbose:
              print(filename, "has wrong extension.")
            if options.delete:
              if options.verbose:
                print("Deleting", filename)
              os.remove(filepath)
            elif options.fix:
              if options.verbose:
                print("Renaming", filepath, "to", split_tup[0]+'.'+kind.extension)
              os.rename(filepath, split_tup[0]+'.'+kind.extension)
            count += 1
    if options.recursive:
      for dir in dirs:
        if options.verbose:
          print("Checking dir:", dir)
    else: #Prevent descending into subfolders
      break          

  if options.count and options.delete:
    print(count, "files with wrong extension deleted.")
    if num_unknown > 0:
      print(num_unknown, "files found with unknown extensions.")
  elif options.count and options.fix:
    print(count, "files with wrong extension fixed.")
    if num_unknown > 0:
      print(num_unknown, "files found with unknown extensions.")
  elif options.count:
    print(count, "files found with wrong extension.")
    if num_unknown > 0:
      print(num_unknown, "files found with unknown extensions.")
########## END MAIN ##########

if __name__ == '__main__':
  main()
