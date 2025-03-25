import argparse
import os
import sys
import plexapi
from datetime import datetime

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

# Constants
plexEnvVarName = "PLEX-TOKEN"

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-T", "--TOKEN", help = "Plex token for connection to API", type=str)
parser.add_argument("-l", "--Library", help = "Plex library name (eg, 'Movies', also default)", type=str, default="Movies")
parser.add_argument("-t", "--Title", help = "Movie title for backdating")
parser.add_argument("-p", "--Plexid", help = "Movie Plex ID for backdating (eg like: 'plex://movie/nnnnnnnnnn')")
parser.add_argument("-g", "--Guid", help = "Movie GUID for finding the item (eg like: 'imdb://ttnnnnnnnn')")
parser.add_argument("-r", "--Release", help = "Use original release date as the 'date added' date", action='store_true')
parser.add_argument("-N", "--RightNow", help = "Use the time and date right now as the 'date added' date", action='store_true')
parser.add_argument("-d", "--Date", help = "New Date for backdating. Defaults to 2018-08-21 11:19:43", type=str, default="2018-08-21 11:19:43")
parser.add_argument("-b", "--BaseURL", help = "BaseURL for Plex connection. Defaults to 'http://localhost:32400'", type=str, default='http://localhost:32400')
parser.add_argument("-n", "--Number", help = "Number of items to be concerned with.", type=int)
parser.add_argument("-y", "--Confirm", help = "Confirms doing the action on all displayed output.", action='store_true')

# Read arguments from command line
args = parser.parse_args()

if not args.TOKEN and not (plexEnvVarName in os.environ):
    # Neither Exist, bail
    print(bcolors.FAIL + "    No PLEX TOKEN (-T XXXXXX) given" + bcolors.ENDC)
    sys.exit(2)
elif not args.TOKEN and (plexEnvVarName in os.environ):
    # env var exists, but token not supplied. use env var data
    print("* Using Token from env var '" + plexEnvVarName + "'")
    args.TOKEN = os.environ.get(plexEnvVarName)
#elif args.TOKEN:
#    # argument given, set/replace environment var, use it
#    print("* Using Token from arguments, saving in env var '" + plexEnvVarName + "'")
#    os.environ[plexEnvVarName] = args.TOKEN

if not args.Library:
    print(bcolors.FAIL + '    No Library (-l "Movies") given' + bcolors.ENDC)
    sys.exit(2)

if not args.Title and not args.Plexid and not args.Guid and not args.Number:
    print(bcolors.FAIL + '    No Title (-t "Title") or Plex ID (-p "PLEXID") or GUID (-g "agent://nnnnnnn") given.' + bcolors.ENDC)
    sys.exit(2)

if not args.Date and not args.Release and not args.RightNow:
    print(bcolors.FAIL + '    No Date (-t "date") given, and neither --RightNow nor --Release selected.' + bcolors.ENDC)
    sys.exit(2)

if not args.BaseURL:
    print(bcolors.FAIL + '    No BaseURL (-b "http://localhost:32400") given.' + bcolors.ENDC)
    sys.exit(2)

from plexapi.server import PlexServer

plex = PlexServer(args.BaseURL, args.TOKEN)
library = plex.library.section(args.Library)
# returns the library/section type, one of 'libtype' eg: movie, show, episode, artist, album, track
# (in case its useful later)
sectionType = library.TYPE

# Find the requested things, return a list.
if args.Title:
    searchList = library.search(title=args.Title)
elif args.Plexid:
    searchList = library.search(guid=args.Plexid)
elif args.Guid:
    searchList = library.getGuid(args.Guid)
elif args.Number:
    searchList = library.recentlyAdded(maxresults=args.Number)

# If search returns one (becomes native object type) correct to list of one, display it, correct plural
if not isinstance(searchList,list):
    searchList = [searchList]
    print(bcolors.OKCYAN + " * Found " + str(len(searchList)) + " " + str(sectionType) + bcolors.ENDC)
else:
    print(bcolors.OKCYAN + " * Found " + str(len(searchList)) + " " + str(sectionType) + "s" + bcolors.ENDC)

# Iterate results
for i, val in enumerate(searchList):
    print(bcolors.OKCYAN + "" + str(i + 1).rjust(6, ' ') + bcolors.ENDC + ": " + bcolors.BOLD + val.title + bcolors.ENDC + " (" + str(val.originallyAvailableAt.year) + ")")
    print("           Title: " + str(val.title))
    print("        Released: " + str(val.originallyAvailableAt))
    print("           Added: " + str(val.addedAt))
    print("         Plex ID: " + str(val.guid))
    previousDate = val.addedAt
    for k, guid in enumerate(val.guids):
        print("        GUID[" + str(k + 1).zfill(2) + "]: " + str(guid.id))

    # Find the exact match, avoid any text matching issues with the API eg duplicates.
    item = library.getGuid(val.guid)
    if isinstance(item,list):
        print(bcolors.FAIL + "Something went wrong. Finding single item from search results returned a set again. " + str(type(item)) + bcolors.ENDC)
        sys.exit(3)

    # Prepare Replacement Date - in loop in case it needs to be different for a given title
    newDate = args.Date
    if args.Release:
        newDate = val.originallyAvailableAt
    elif args.RightNow:
        newDate = datetime.now().replace(microsecond=0)

    # Store the value in the update variable
    updates = {"addedAt.value": newDate}

    if args.Confirm:
        # Write the change if we should
        item.edit(**updates)

        # Get the item from the DB again and see what it was set to
        changeditem = library.getGuid(val.guid)
        changedDate = changeditem.addedAt
        print(bcolors.WARNING + "      ! Date changed from " + str(previousDate) +  " to " + str(changedDate) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "      ! Date would have changed from " + str(previousDate) +  " to " + str(newDate) + bcolors.ENDC)

    # Newline For Each Row
    print(" ")

# Newline on completion
#print(" ")
