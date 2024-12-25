# Plex Scripts
Some minor scripts for plex that made my life a million times better

## Modify or remove items from the 'recently added' list
This feature doesn't exist in the UI, and googling a bit, it has had only a few mentions, but from a long time ago.  Just before I kicked off editing the DB already, I found a neat post from a guy who shared the basics of some python to remove a title from the list.  Problem for me was that there were 100's because I just removed a lot of duplicate files. (For some unknown reason, manually deleting a file causes the title to come back to the very front of the "recently added" list.  The original code seemed to work, but not all the time.  And not so easily on titles with Chinese characters etc.  On items with the same name from different years, it also did not work.  So I had a crack at making it better.  
* Original link/idea: https://www.reddit.com/r/PleX/comments/11svszf/remove_movie_from_recently_added/
* Plex Python library: https://python-plexapi.readthedocs.io/en/latest/introduction.html

### Prerequisites
- Get yourself python installed. (Better instructions exist elsewhere for this than I am currently capable of!)
- You will need to install python Plex API (above link).
- You will need a Plex Token for authentication purposes.
 
### To make it work
The script works by assembling a query/list of things to set a date on.  It will return other identifiers (plex GUID, IMDB GUID, etc) for the titles you find, in case there are more than one.  You can run it again against specific ones by using the actual IDs if you need.  Alternatively, run it with an -n, and it will show the last n results.  Without the required switch below, it will display what it will do.  When you are happy with the items found, the confirm switch below to make it do the work.
Run the 'modifyRecentlyAdded.py' script and use the following switches (Case Sensitive):
- -T (--TOKEN): get yourself a Plex Token for authentication.
- -l (--Library):  I thought I was going to use this, unimplemented for now. Plex library name (eg, 'Movies', also default)", type=str, default="Movies"
- -t (--Title): Movie title for searching
- -p (--Plexid): Movie Plex ID for searching (eg like: 'plex://movie/nnnnnnnnnn')
- -g (--Guid): Movie agent identifier/GUID for finding the item (eg like: 'imdb://ttnnnnnnnn')
- -d (--Date): New Date for setting the 'addedAt' to.  Defaults to "2018-08-21 11:19:43" if you don't set one.
- -b (--BaseURL): BaseURL for Plex connection. Defaults to 'http://localhost:32400'.
- -n (--Number): Number of items in the recently added list to operate on.
- -y (--Confirm): Confirms doing the action on the displayed output.  Script will not make changes without it.
Purpose of the script is to have you find what items you want addressed, then run it.
### Extra Notes
- Dates in the future will work.
- Haven't tried it against tv shows yet.  I suspect it might want a bit more work and a few more options, however, this is a starter for 10.
- This is my first foray into Python, and indeed posting anything to Github.  AKA: I have proper script kiddied this up.  I googled what I needed when I needed, to start understanding Python syntax.  I have had success, please try it as you wish, I'll happily take any feedback.
