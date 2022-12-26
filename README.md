# file-extension-corrector
A tool used to make sure that files really are what their extensions say they are.

Run with: `{Python Path} correctext.py [options]`

*****

Required flags: --type (-t) or --rename (-R)

*****

--type: File type(s) to check for. Comma delimited (e.g. -t jpg,png). Input * for all.

Examples:

`{Python Path} correctext.py -t *` checks every file

`{Python Path} correctext.py -t jpg,png` checks all files of actual type jpeg or png

*****

--recursive: Check files in subdirectories as well.

Examples:

`{Python Path} correctext.py -t * -r` checks every file including those in subfolders.

`{Python Path} correctext.py -t jpg,png -r` checks all files of actual type jpeg or png including those in subfolders.

*****

Note: Requires filetype.py
Use `pip install filetype`

Tool created by: Elgin Ciani
