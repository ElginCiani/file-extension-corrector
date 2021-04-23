# file-extension-checker
A tool used to make sure that files really are what their extensions say they are.

Run with: `{Python Path} checkext.py [options]`

*****

Required flags: --type (-t) or --rename (-R)

*****

--type: File type(s) to check for. Comma delimited (e.g. -t jpg,png). Input * for all.

Examples:

`{Python Path} checkext.py -t *` checks every file

`{Python Path} checkext.py -t jpg,png` checks all files of actual type jpeg or png

*****

--recursive: Check files in subdirectories as well.

Examples:

`{Python Path} checkext.py -t * -r` checks every file including those in subfolders.

`{Python Path} checkext.py -t jpg,png -r` checks all files of actual type jpeg or png including those in subfolders.

*****

Note: Requires filetype.py
Use `pip install filetype`

Tool created by: Elgin Ciani
