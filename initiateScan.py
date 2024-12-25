import argparse
import os
import sys
import plexapi
import itertools
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-T", "--TOKEN", help = "Plex token for connection to API", type=str)
parser.add_argument("-l", "--Library", help = "Plex library name (eg, 'Movies', also default)", type=str, default="Movies")
parser.add_argument("-b", "--BaseURL", help = "BaseURL for Plex connection. Defaults to 'http://localhost:32400'", type=str, default="http://localhost:32400")
parser.add_argument("-c", "--Cancel", help = "Cancels the initiated Scan.", action='store_true')
parser.add_argument("-p", "--Path", help = "Specify the Path for Update")

# Read arguments from command line
args = parser.parse_args()

if not args.TOKEN:
    print(bcolors.FAIL + "    No PLEX TOKEN (-T XXXXXX) given" + bcolors.ENDC)
    sys.exit(2)

if not args.Library:
    print(bcolors.FAIL + '    No Library (-l "Movies") given' + bcolors.ENDC)
    sys.exit(2)

from plexapi.server import PlexServer

# Connect to the Plex Library
plex = PlexServer(args.BaseURL, args.TOKEN)
library = plex.library.section(args.Library)
sectionType = library.TYPE

# Kick Off Scan
if args.Cancel:
    output = library.cancelUpdate()
elif args.Path:
    output = library.update(args.Path)
else:
    output = library.update()
