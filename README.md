# Plex Scripts
Some minor scripts for plex that made my life a million times better

## Modify or remove items from the 'recently added' list
This feature doesn't exist in the UI, and googling a bit, it has had only a few mentions, but from a long time ago.  Just before I kicked off editing the DB directly, I found a neat post from a guy who shared the basics of some python to remove a title from the list.  Problem for me was that there were 100's because I just removed a lot of duplicate files. (For some unknown reason, manually deleting a duplicated source file causes plex to completely rescan, and the item comes back to the very front of the "recently added" list.  The sample code I found seemed to work, but not all the time.  After some digging, it was when items had similar names, but different years, or titles with Chinese characters, etc.  So I had a crack at doing something better.  
* [Original link/idea](https://www.reddit.com/r/PleX/comments/11svszf/remove_movie_from_recently_added/)
* [Plex Python library](https://python-plexapi.readthedocs.io/en/latest/introduction.html)

### Prerequisites
Better instructions exist elsewhere for all of these.  I'll link them, where I can.
- Get yourself python installed.
- You will need to install [Plex Python library](https://python-plexapi.readthedocs.io/en/latest/introduction.html)
- You will need a [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) for authentication purposes in this version.  (There is a username/password method which I may implement later, however I have 2FA and I don't believe that works with this.)
 
### To make it work
The script works by assembling a query/list of things to set a date on.  It will return other identifiers (plex GUID, IMDB GUID, etc) for the titles you find, in case there are more than one.  You can run it again against specific ones by using the actual IDs if you need.  Alternatively, run it with an -n, and it will show the last n results.  Without the required 'confirm' switch below, it will only display what it would do.  When you are happy with the items found, include the the confirm switch to make it actually do the work.
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
If your data for a switch has a space in it, you will need to specify it in double quotes.

### Extra Notes
- Dates in the future will work.
- Haven't tried it against tv shows yet.  I suspect it might want a bit more work and a few more options, however, this is a starter for 10.
- This is my first foray into Python, and indeed posting anything to Github.  AKA: I have proper script kiddied this up.  I googled what I needed when I needed, to start understanding Python syntax.  I have had success, please try it as you wish, I'll happily take any feedback.

### Examples
Example 1: see most recent 3 items on the Recently Added list.  Note the text shows what would have happened as the confirm switch was not supplied:
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -n 3 -T YOURTOKENGOESHERE
 * Found 3 movies
   - [0] Movie Title Number One (1990)
      Added at: 2024-12-23 03:55:53
      Plex ID: plex://movie/6234353454ccb34a1cf31d465fad
      GUID[0]: imdb://tt2723452640
      GUID[1]: tmdb://104234453905
      GUID[2]: tvdb://33603234502
      ! Date would have changed from 2024-12-23 03:55:53 to 2018-08-21 11:19:43
   - [1] Movie Title Number One (2024)
      Added at: 2024-12-23 03:48:53
      Plex ID: plex://movie/641c04c7bf014a24aed9ed0e
      GUID[0]: imdb://tt60212719
      GUID[1]: tmdb://2493110
      GUID[2]: tvdb://399653
      ! Date would have changed from 2024-12-23 03:48:53 to 2018-08-21 11:19:43
   - [2] Some other movie title here (2021)
      Added at: 2024-12-23 03:39:05
      Plex ID: plex://movie/6c2896a40eb6694d3de7886b
      GUID[0]: imdb://tt32627545
      GUID[1]: tmdb://1522996
      GUID[2]: tvdb://365748
      ! Date would have changed from 2024-12-23 03:39:05 to 2018-08-21 11:19:43

[user@server plexscripts]$
```
Example 2: Because the first two results are the same title, I'm specifying one by its plex ID.  Note that this time the work is actually done with the final switch (noted on the last line):
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -T YOURTOKENGOESHERE -p plex://movie/6234353454ccb34a1cf31d465fad -y
 * Found 1 movie
   - [0] Movie Title Number One (1990)
      Added at: 2024-12-23 03:55:53
      Plex ID: plex://movie/6234353454ccb34a1cf31d465fad
      GUID[0]: imdb://tt2723452640
      GUID[1]: tmdb://104234453905
      GUID[2]: tvdb://33603234502
      ! Date changed from 2024-12-23 03:55:53 to 2018-08-21 11:19:43

[user@server plexscripts]$
```

Example 3: Will return any title in your Movie library beginning with "Lord".  This will include any 'lord of the rings' or 'lord of the flies', etc etc.  Note that if you specify the year as part of the title, it will not be found since Plex stores this value separately from the title:
```console
[user@server plexscripts]$ python3 modifyRecentlyAdded.py -T YOURTOKENGOESHERE -t "Lord"
```

### Things to do when I get better at Python:
- Clean up syntax checking for dates
- Test and fix for TV series checking also
- adjust the default token to come from environment variables, like: ```os.environ.get("PLEX_TOKEN")```


## Lastly [Disclaimer]:
- I don't expect that anything could go wrong using these methods.  They seem far safer than messing with the Sqlite db directly, especially since Plex have modified the executable somehow.  All this said, your mileage may vary.  I have taken all care possible, but make no guarantees - all responsibility is yours!
