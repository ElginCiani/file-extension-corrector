#!/usr/bin/env python3
import os
import optparse
import subprocess
import filetype

#Initialize Variables
count = 0
num_unknown = 0
num_renames = 0
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
    version="%prog 1.2")

  #Available command line arguments
  parser.add_option("-t", "--type", dest="type", action="append", type="string", help="File type(s) to check for. Comma delimited (e.g. -t jpg,png). Input * for all.")
  parser.add_option("-d", "--delete", dest="delete", action="store_true", default=False, help="Delete file if the extension does not match true file type.")
  parser.add_option("-f", "--fix", dest="fix", action="store_true", default=False, help="Rename file extension if it does not match true file type.")
  parser.add_option("-r", "--recursive", dest="recursive", action="store_true", default=False, help="Check files in subdirectories as well.")
  parser.add_option("-R", "--rename", dest="rename", action="append", type="string", help="Renames all extensions from a to b (i.e. -R a,b).")
  parser.add_option("-l", "--lowercase", dest="lowercase", action="store_true", default=False, help="Sets all file extensions to lowercase if used by itself. Sets rename to use lowercase extensions when used with --fix (default).")
  parser.add_option("-u", "--uppercase", dest="uppercase", action="store_true", default=False, help="Sets all file extensions to uppercase if used by itself. Sets rename to use uppercase extensions when used with --fix.")
  parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help="Enable this flag to turn off any print logging.")
  parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Enable this flag for extra logging.")
  
  global options
  (options, arguments) = parser.parse_args()

  #Throw error if user does not specify required parameters
  if not options.type and not options.rename and not options.lowercase and not options.uppercase:
    parser.error("[-] Please specify file type(s). Use * to check all. See --help for more info.")
  elif options.rename and (options.delete or options.fix):
    parser.error("[-] Do not set --rename flag along with --delete or --fix.")
  elif options.type and options.rename:
    parser.error("[-] Do not set --type and --rename flags simultaneously.")
  elif options.delete and options.fix:
    parser.error("[-] Do not set --delete and --fix flags simultaneously.")
  elif options.lowercase and options.uppercase:
    parser.error("[-] Dor not set --lowercase and --uppercase flags simultaneously.")
  elif options.quiet and options.verbose:
    parser.error("[-] Do not set --quiet and --verbose flags simultaneously.")
  ## End: Error scenarios ##
  return options


def rename():
  global num_renames
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
        num_renames += 1
    if options.recursive:
      for dir in dirs:
        if options.verbose:
          print("Checking dir:", dir)
    else: #Prevent descending into subfolders
      break


def change_case(types):
  global num_renames
  if options.lowercase:
    if options.verbose:
      print("Changing all specified file extensions to lowercase.")
    for root, dirs, files in os.walk("."):
      for filename in files:
        if '*' in types:
          filepath = root+"\\"+filename
          split_tup = os.path.splitext(filepath)
          new_name = split_tup[0]+'.'+filename.rsplit('.', 1)[1].lower()
          if options.verbose:
            print("Renaming", filepath, "to", new_name)
          os.rename(filepath, new_name)
          num_renames += 1
        else:
          for extension in types:
            filepath = root+"\\"+filename
            split_tup = os.path.splitext(filepath)
            if split_tup[1][1:].lower() == extension.lower():
              new_name = split_tup[0]+'.'+extension.lower()
              if options.verbose:
                print("Renaming", filepath, "to", new_name)
              os.rename(filepath, new_name)
              num_renames += 1
      if options.recursive:
        for dir in dirs:
          if options.verbose:
            print("Checking dir:", dir)
      else: #Prevent descending into subfolders
        break
  else: #options.uppercase
    if options.verbose:
      print("Changing all specified file extensions to uppercase.")
    for root, dirs, files in os.walk("."):
      for filename in files:
        if '*' in types:
          filepath = root+"\\"+filename
          split_tup = os.path.splitext(filepath)
          new_name = split_tup[0]+'.'+filename.rsplit('.', 1)[1].upper()
          if options.verbose:
            print("Renaming", filepath, "to", new_name)
          os.rename(filepath, new_name)
          num_renames += 1
        else:
          for extension in types:
            filepath = root+"\\"+filename
            split_tup = os.path.splitext(filepath)
            if split_tup[1][1:].upper() == extension.upper():
              new_name = split_tup[0]+'.'+extension.upper()
              if options.verbose:
                print("Renaming", filepath, "to", new_name)
              os.rename(filepath, new_name)
              num_renames += 1
      if options.recursive:
        for dir in dirs:
          if options.verbose:
            print("Checking dir:", dir)
      else: #Prevent descending into subfolders
        break


########## MAIN ##########
def main():
  global count
  options = parse_args() #Option parser

  #User just wants to rename files
  if options.rename and not options.type:
    rename()
    if not options.quiet:
      print(num_renames, "files renamed.")
    return
  
  types = options.type[0].split(",") #Array of specified types

  #User wants to change extension casing
  if (options.lowercase or options.uppercase):
    change_case(types)

  #Check all files
  for root, dirs, files in os.walk("."):
    for filename in files:
      if options.verbose:
        print("Checking file:", filename)
      filepath = root+"\\"+filename
      split_tup = os.path.splitext(filepath)
      kind = filetype.guess(filepath)
      if kind is None:
        if options.verbose:
          print('Cannot guess file type!')
        continue
      else:
        if options.verbose:
          print('File extension: %s' % kind.extension)
          print('File MIME type: %s' % kind.mime)
        if '*' in types or kind.extension in types:
          if kind.extension != split_tup[1][1:].lower(): #File extension is wrong
            if not options.quiet:
              print(filename, "has wrong extension.")
            if options.delete:
              if options.verbose:
                print("Deleting", filename)
              os.remove(filepath)
            elif options.fix:
              if options.uppercase:
                new_name = split_tup[0]+'.'+kind.extension.upper()
              else:
                new_name = split_tup[0]+'.'+kind.extension.lower()
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

  #Final print logging
  if options.delete and not options.quiet:
    print(count, "files with wrong extension deleted.")
  elif options.fix and not options.quiet:
    print(count, "files with wrong extension fixed.")
  elif not options.delete and not options.fix and not options.quiet:
    print(count, "files found with wrong extension.")
  if not options.quiet:
    if num_renames > 0:
      print(num_renames, "file extensions parsed.")
    if num_unknown > 0:
      print(num_unknown, "files found with unknown extensions.")
########## END MAIN ##########

if __name__ == '__main__':
  main()
