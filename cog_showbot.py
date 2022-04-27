from twitchio.ext import commands
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SHOWBOT_KEY = os.environ.get('SHOWBOT_KEY') or "get-your-showbot.tv-key"

# A Twitchio "Cog" class for plugging into a Twitchio bot that supports ShowBot commands
# "Empower your Twitch chat to submit ideas, show titles,questions and more, '
#  then vote the best to the top."
# http://showbot.tv
#
# Put your showbot key (https://www.showbot.tv/s/login/setup.php) into the .env file as
# SHOWBOT_KEY="whatever your key is"
# Do not show your SHOWBOT_KEY on stream.  
# 
# This registers commands (assuming "!" as the bot command prefix"): 
# !s Title : user submission for title/whatever to showbot
# !showbot : reminder message about showbot
# !showbotreset : Delete all showbot titles (mods/broadcaster only)
# !showbotdelete <id number> : Delete specific id showbot entry (mods/broadcaster only)
class ShowbotCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print(f"Showbot key is {SHOWBOT_KEY}")

    @commands.command(name="s")
    async def showbot_submit(self, ctx: commands.Context):
        showbot_raw = ctx.message.content
        showbot_author = ctx.author.display_name
        showbot_channel = ctx.channel.name
        showbot_title_list = showbot_raw.split(" ",1)
        if len(showbot_title_list) <= 1:
            print("no title submitted")
            return 
        showbot_title=showbot_title_list[1]
        payload = {"title": showbot_title,
                   "user": showbot_author,
                   "channel": showbot_channel,
                   "key": SHOWBOT_KEY}
        try:
            showbot_url = requests.get("http://www.showbot.tv/s/add.php", params=payload)
        except Exception as e:
            print(f"There was a showbot problem [{e}]")
            ctx.send("Sorry, showbot not responding")
            return 
        channel_name = ctx.channel.name
        await ctx.send(f"{showbot_url.text}. https://{channel_name}.showbot.tv to vote")

    @commands.command(name="showbotdelete")
    async def showbot_delete_item(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            showbot_deleted_item = ctx.message.content.split(" ",1)
            if len(showbot_deleted_item) <= 1:
                print("nothing to delete submitted")
                await ctx.send(f"{ctx.author.display_name}, this is to delete single showbot items.  Maybe you want !showbotreset")
                return 
            payload = {"channel": ctx.channel.name,
                        "key": SHOWBOT_KEY,
                        "id": showbot_deleted_item}
            try:
                showbot_delete_url = requests.get("http://www.showbot.tv/s/delete.php", params=payload)
            except Exception as e:
                print(f"There was a showbot problem [{e}]")
                ctx.send("Sorry, showbot not responding")
                return 
            await ctx.send(showbot_delete_url.text)
        else:
            print(f"{ctx.author.display_name} is not on the showbot authorization list")

    @commands.command(name="showbot")
    async def showbot_reminder(self, ctx: commands.Context):
        channel_name = ctx.channel.name
        reminder_text = f"Use !s [your submission] to submit items to be voted on. Go to https://{channel_name}.showbot.tv to vote!"
        await ctx.send(reminder_text)

    @commands.command(name="showbotreset")
    async def showbot_reset(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            payload = {"channel": ctx.channel.name,
                        "key": SHOWBOT_KEY}
            try:
                showbot_reset_url = requests.get("http://www.showbot.tv/s/reset.php", params=payload)
            except Exception as e:
                print(f"There was a showbot problem [{e}]")
                ctx.send("Sorry, showbot not responding")
                return 
            await ctx.send(showbot_reset_url.text)
        else:
            print(f"{ctx.author.display_name} is not on the showbot authorization list")