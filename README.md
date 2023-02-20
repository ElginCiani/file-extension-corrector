# file-extension-corrector
A tool used to check and correct file extensions.

Do you have a bunch of images with incorrect file extensions (e.g. A png that says it's a jpeg)?
What about a bunch of INCONSISTENT extension capiTaliZatiON?
Fix that with this tool and make sure files really are what their extensions say they are!

Run with: `python3 correctext.py [options]`

Note: Requires python3 and filetype.py

Use `pip install filetype`

*****

Required flags: --type (-t) or --rename (-R)

*****

`--type`: File type(s) to check for. Comma delimited (e.g. -t jpg,png). Input * for all.

Examples:

`python3 correctext.py -t *` checks every file

`python3 correctext.py -t jpg,png` checks all files of actual type jpeg or png

*****

`--recursive`: Check files in subdirectories as well.

Examples:

`python3 correctext.py -t * -r` checks every file including those in subfolders.

`python3 correctext.py -t jpg,png -r` checks all files of actual type jpeg or png including those in subfolders.

*****

Note:

To actually fix file extensions instead of just doing a dry run, use the `--fix` flag.

Example:

`python3 correctext.py -r -f -t *` fixes every file extension

*****

Other features include:

`-R, --rename`: Renames all extensions from a to b (i.e. -R a,b).

`-l, --lowercase`: Sets all file extensions to lowercase if used by itself. Sets rename to use lowercase extensions when used with --fix (default).

`-u, --uppercase`: Sets all file extensions to uppercase if used by itself. Sets rename to use uppercase extensions when used with --fix (default).

`-d, --delete`: Delete file if the extension does not match true file type.

`-q, --quiet` and `-v, --verbose` options.

*****

Tool created by: Elgin Ciani
