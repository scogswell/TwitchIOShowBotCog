# TwitchIOShowBotCog
A Cog for bots based on Twitchio (https://github.com/TwitchIO/TwitchIO) to use Showbot, http://showbot.tv
 
Showbot.tv is a service that allows twitch viewers to submit and vote on titles (or whatever thing you'd
like them to submit and vote on).  Showbot.tv is a free service.  
 
This Cog registers these bot stream commands: (assuming "!" as the bot command prefix"): 

`!s <a clever title>` : user submission for title/whatever to showbot

`!showbot` : reminder message about showbot

`!showbotreset` : Delete all showbot titles (mods/broadcaster only)

`!showbotdelete <id number>` : Delete specific id showbot entry (mods/broadcaster only)

 
 Get a showbot key from showbot.tv, and put it in the file ".env" so it will be loaded automatically
 at startup:
 
 ```
 SHOWBOT_KEY="whatever-your-showbot-key-is"
 ```
 
 
 In your main program, add the Cog as you would normally:
 
 ```python
 from twitchio.ext import commands

from cog_showbot import ShowbotCog

... Whatever your bot setup is in twitchio ...


bot = Bot()
bot.add_cog(ShowbotCog(bot))  # Showbot commands 
bot.run()
 ```
