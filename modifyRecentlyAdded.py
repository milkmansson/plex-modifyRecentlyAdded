import argparse
import os
import sys
import plexapi

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
parser.add_argument("-t", "--Title", help = "Movie title for backdating")
parser.add_argument("-p", "--Plexid", help = "Movie Plex ID for backdating (eg like: 'plex://movie/nnnnnnnnnn')")
parser.add_argument("-g", "--Guid", help = "Movie GUID for finding the item (eg like: 'imdb://ttnnnnnnnn')")
parser.add_argument("-d", "--Date", help = "New Date for backdating. Defaults to 2018-08-21 11:19:43", type=str, default="2018-08-21 11:19:43")
parser.add_argument("-b", "--BaseURL", help = "BaseURL for Plex connection. Defaults to 'http://localhost:32400'", type=str, default='http://localhost:32400')
parser.add_argument("-n", "--Number", help = "Number of items to be concerned with.", type=int)
parser.add_argument("-y", "--Confirm", help = "Confirms doing the action on all displayed output.", action='store_true')

# Read arguments from command line
args = parser.parse_args()

if not args.TOKEN:
    print("No PLEX TOKEN (-T XXXXXX) given")
    sys.exit(2)

if not args.Library:
    print('No Library (-l "Movies") given')
    sys.exit(2)

if not args.Title and not args.Plexid and not args.Guid and not args.Number:
    print('No Title (-t "Title") or Plex ID (-p "PLEXID") or GUID (-g "agent://nnnnnnn") given')
    sys.exit(2)

if not args.Date:
    print('No Date (-t "date") given')
    sys.exit(2)

if not args.BaseURL:
    print('No BaseURL (-b "http://localhost:32400") given')
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
    print(" * Found " + str(len(searchList)) + " " + str(sectionType))
else:
    print(" * Found " + str(len(searchList)) + " " + str(sectionType) + "s)")

# Prepare Update dict content
updates = {"addedAt.value": args.Date}

# Iterate results
for i, val in enumerate(searchList):
    print("   - [" + str(i) + "] " + bcolors.BOLD + val.title + bcolors.ENDC)
    print("      Added at: " + str(val.addedAt))
    print("      Plex ID: " + str(val.guid))
    previousDate = val.addedAt
    for k, guid in enumerate(val.guids):
        print("      GUID[" + str(k) + "]: " + str(guid.id))

    # Find the exact match, avoid any text matching issues with the API eg duplicates.
    item = library.getGuid(val.guid)
    if isinstance(item,list):
        print("Something went wrong. Finding single item from search results returned a set again. " + str(type(item)) )
        sys.exit(3)

    if args.Confirm:
        item.edit(**updates)
        changeditem = library.getGuid(val.guid)
        newDate = changeditem.addedAt
        print(bcolors.WARNING + "      ! Date changed from " + str(previousDate) +  " to " + str(newDate) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "      ! Date would have changed from " + str(previousDate) +  " to " + str(args.Date) + bcolors.ENDC)

# Newline on completion
print(" ")
