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

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def prettySize(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

# Initialize parser
parser = argparse.ArgumentParser()


# Adding optional argument
parser.add_argument("-T", "--TOKEN", help = "Plex token for connection to API", type=str)
parser.add_argument("-l", "--Library", help = "Plex library name (eg, 'Movies', also default)", type=str, default="Movies")
parser.add_argument("-b", "--BaseURL", help = "BaseURL for Plex connection. Defaults to 'http://localhost:32400'", type=str, default="http://localhost:32400")
parser.add_argument("-n", "--Number", help = "Number of items to be concerned with.", type=int)
parser.add_argument("-y", "--Confirm", help = "Confirms doing the action on all displayed output.", action='store_true')

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

# Query for the Duplicates
duplicatesList = library.search(duplicate="True")

if args.Number:
    for item in itertools.islice(duplicatesList,args.Number):
        print("     " + item.title)
        for j, file in enumerate(item.media):
            print("     - [" + str(j) + "] " + file.parts[0].file + "  " + prettySize(file.parts[0].size) )

else:
    for i, item in enumerate(duplicatesList):
        print("    " + str(i) + " " + item.title)
        for j, file in enumerate(item.media):
            print("     - [" + str(j) + "] " + file.parts[0].file + "  " + prettySize(file.parts[0].size) )
