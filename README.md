# Plex Scripts
Some minor scripts for plex that made my life a million times better

## [modifyRecentlyAdded.py] Modify or remove items from the 'recently added' list
This feature doesn't exist in the UI, and googling a bit, it has had only a few mentions, but from a long time ago.  Just before I kicked off editing the DB directly, I found a neat post from a guy who shared the basics of some python to remove a title from the list.  Problem for me was that there were 100's because I just removed a lot of duplicate files. (For some unknown reason, manually deleting a duplicated source file causes plex to completely rescan, and the item comes back to the very front of the "recently added" list.  The sample code I found seemed to work, but not all the time.  After some digging, it was when items had similar names, but different years, or titles with Chinese characters, etc.  So I had a crack at doing something better.  
* [Original link/idea](https://www.reddit.com/r/PleX/comments/11svszf/remove_movie_from_recently_added/)
* [Plex Python library](https://python-plexapi.readthedocs.io/en/latest/introduction.html)

### Prerequisites
Better instructions exist elsewhere for all of these.  I'll link them, where I can.
- Get yourself python installed.
- You will need to install [Plex Python library](https://python-plexapi.readthedocs.io/en/latest/introduction.html)
- You will need a [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) for authentication purposes in this version.  (There is a username/password method which I may implement later, however I have 2FA and I don't believe that works with this.)  Additional info [here](https://www.plexopedia.com/plex-media-server/general/plex-token/).
 
### To make it work
The script works by assembling a query/list of things to set a date on.  It will return other identifiers (plex GUID, IMDB GUID, etc) for the titles you find, in case there are more than one.  You can run it again against specific ones by using the actual IDs if you need.  Alternatively, run it with an -n, and it will show the last n results.  Without the required 'confirm' switch below, it will only display what it would do.  When you are happy with the items found, include the the confirm switch to make it actually do the work.
Run the 'modifyRecentlyAdded.py' script and use the following switches (Case Sensitive):
##### Setup:
- -T (--TOKEN): get yourself a Plex Token for authentication.
- -l (--Library):  I thought I was going to use this, unimplemented for now. Plex library name (eg, 'Movies', also default)", type=str, default="Movies"
- -b (--BaseURL): BaseURL for Plex connection. Defaults to 'http://localhost:32400'
##### Selectors:
- -t (--Title): Movie title for searching
- -p (--Plexid): Movie Plex ID for searching (eg like: 'plex://movie/nnnnnnnnnn')
- -g (--Guid): Movie agent identifier/GUID for finding the item (eg like: 'imdb://ttnnnnnnnn')
- -n (--Number): Number of items in the recently added list to operate on.
##### Setting the DateTime value:
- -d (--Date): Give the new date for setting the 'addedAt' to.  Defaults to "2018-08-21 11:19:43" if you don't set one.  Useful for pushing things forward or back in the list as far as desired.
- -r (--Release): Set the 'addedAt' to the item's 'originallyAvailableAt' value.  (Essentially the cinematic release date, normally as found by the Plex Agent.)  Useful for a sensible push back.
- -N (--RightNow): Set the 'addedAt' date to the the datetime right now.  Useful for bringing the item forward from the past.
##### Write Switch:
- -y (--Confirm): Confirms doing the action on the displayed output.  Script will not make any adjustments without this switch being set.

### Extra Notes
- If your data for a switch has a space in it, you will need to specify it in double quotes.
- Dates in the future will work, and this will have the obvious result of puting the title further forward in the list.  Plex adding something today, where your item is a year in the future, will have the result of plex's new item coming second, until that year passes.
- Haven't tried it against tv shows yet.  I suspect it might want a bit more work and a few more options, however, this is a starter for 10.
- This is my first foray into Python, and indeed posting anything to Github.  AKA: I have proper script kiddied this up.  I googled what I needed when I needed, to start understanding Python syntax.  I have had success, please try it as you wish, I'll happily take any feedback.

### Examples
Example 1: see most recent 3 items on the Recently Added list.  Note the text shows what would have happened as the confirm switch was not supplied:
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -n 3 -T YOURTOKENGOESHERE
 * Found 3 movies
   - [0] Movie Title Number One (1990)
      Added at: 2024-12-23 03:55:53
      Plex ID: plex://movie/634a1cf31d465234353454ccb34a1cf31d465f
      GUID[0]: imdb://tt27234526407234
      GUID[1]: tmdb://1053905425390534
      GUID[2]: tvdb://3360539055390532
      ! Date would have changed from 2024-12-23 03:55:53 to 2018-08-21 11:19:43
   - [1] Movie Title Number One (2024)
      Added at: 2024-12-23 03:48:53
      Plex ID: plex://movie/641c04c7bf014a24aed9ed0ea1cf31d4652343
      GUID[0]: imdb://tt60253905153905
      GUID[1]: tmdb://2495390531539051
      GUID[2]: tvdb://3953905953905653
      ! Date would have changed from 2024-12-23 03:48:53 to 2018-08-21 11:19:43
   - [2] Some other movie title here (2021)
      Added at: 2024-12-23 03:39:05
      Plex ID: plex://movie/6c2896a40eb6694d3de7886ba1cf31d4652343
      GUID[0]: imdb://tt5453262754522
      GUID[1]: tmdb://152299622992299
      GUID[2]: tvdb://365748229922995
      ! Date would have changed from 2024-12-23 03:39:05 to 2018-08-21 11:19:43

[user@server plexscripts]$
```
Example 2: Because the first two results are the same title, I'm specifying one by its plex ID.  Note that this time the work is actually done with the final switch (noted on the last line):
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -T YOURTOKENGOESHERE -p plex://movie/62343531cf31d465454ccb34afad -y
 * Found 1 movie
   - [0] Movie Title Number One (1990)
      Added at: 2024-12-23 03:55:53
      Plex ID: plex://movie/62343531cf31d465454ccb34afad
      GUID[0]: imdb://tt27234526407234
      GUID[1]: tmdb://1053905425390534
      GUID[2]: tvdb://3360539055390532
      ! Date changed from 2024-12-23 03:55:53 to 2018-08-21 11:19:43

[user@server plexscripts]$
```

Example 3: Will return any title in your Movie library containing "Lord".  This will include any 'lord of the rings', 'lord of the flies', 'sealord', etc etc.  Note that if you specify the year as part of the title, it will not be found since Plex stores this value separately from the title:
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -T YOURTOKENGOESHERE -t "Lord"
```

Example 4: Will set the first 4 things in the 'Recently Added' list to their individual release dates.  Script describes what it would have done, if it had the -y switch, but does not write anything to the database:
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -T YOURTOKENGOESHERE -n 4 -r
 * Found 4 movies
 - [  1] Something I Want to Watch (2016)
         Added: 2025-03-24 20:00:00
      Released: 2016-12-10 00:00:00
       Plex ID: plex://movie/64555f63c345e0f5e83fb3b9
      GUID[01]: imdb://tt255388463405788
      GUID[02]: tmdb://255388463405788
      GUID[03]: tvdb://255388463405788
      ! Date would have changed from 2025-03-24 20:47:33 to 2016-12-10 00:00:00
 - [  2] One Rubbish Film (2025)
         Added: 2025-03-18 16:00:00
      Released: 2025-02-27 00:00:00
       Plex ID: plex://movie/64555f63c345e0f5e83fb3b9
      GUID[01]: imdb://tt255388463405788
      GUID[02]: tmdb://255388463405788
      GUID[03]: tvdb://255388463405788
      ! Date would have changed from 2025-03-18 16:08:34 to 2025-02-27 00:00:00
 - [  3] Some Other Title (2006)
         Added: 2025-03-15 04:00:00
      Released: 2006-09-12 00:00:00
       Plex ID: plex://movie/64555f63c345e0f5e83fb3b9
      GUID[01]: imdb://tt255388463405788
      GUID[02]: tmdb://255388463405788
      GUID[03]: tvdb://255388463405788
      ! Date would have changed from 2025-03-15 04:09:16 to 2006-09-12 00:00:00
 - [  4] Title Awesome (2024)
         Added: 2025-03-07 18:00:00
      Released: 2024-12-17 00:00:00
       Plex ID: plex://movie/64555f63c345e0f5e83fb3b9
      GUID[01]: imdb://tt255388463405788
      GUID[02]: tmdb://255388463405788
      ! Date would have changed from 2025-03-07 18:17:01 to 2024-12-17 00:00:00
```

### Things to do when I get better at Python:
- Clean up syntax checking for dates input at the command line
- Add a feature to subtract or add time from the original value, instead of specifying a complete datetime value
- Test and fix for TV series checking also, adding logic for episodes and series
- adjust the default token to come from environment variables, eg, use a value from: ```os.environ.get("PLEX_TOKEN")```



## [initiateScan.py] Initiate a library Scan
_Still a work in progress_ After deleting a bunch of source files, it could take a while before the system registered that they were missing, and then to have them show up in the Recently Added list.  This initiates a library scan. (A quick thing, and not a refresh of metadata etc.)

## Lastly [Disclaimer]:
- I don't expect that anything could go wrong using these methods.  They seem far safer than messing with the Sqlite db directly, especially since Plex have modified the executable somehow.  All this said, your mileage may vary.  I have taken all care possible, but make no guarantees - all responsibility is yours!
