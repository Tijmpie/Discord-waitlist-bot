import discord
import os
import json
import time
from configparser import ConfigParser
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from operator import itemgetter
from pathlib import Path

config = ConfigParser()
config.read("config.cfg")

TOKEN = config.get("bot","token")

bot = commands.Bot(command_prefix=config.get("bot","commandPrefix"))
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Timjim\'s coding skills"))

@bot.command(name="add")
async def _add(ctx, arg):
    if ctx.channel.id == int(config.get("bot","channelID")):
        json_file = Path("data.txt")
        if not json_file.exists():
            with open("data.txt", "w") as file:
                file.write("[]")
        with open("data.txt", "r") as file:
            json_loaded = json.load(file)
        json_loaded.append({"username": arg, "time": int(time.time())})
        with open("data.txt", "w") as file:
            json.dump(json_loaded, file)
            await ctx.send(f"> Player **{arg}** has been added to the waiting list")
    else:
        await ctx.send("This bot is not allowed to be used in this channel!")

@_add.error
async def errorfunction(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument, make sure to input a username")

@bot.command(name="remove")
async def _remove(ctx, arg):
    if ctx.channel.id == int(config.get("bot", "channelID")):
        with open("data.txt", "r") as file:
            data = json.load(file)
        new_data = [d for d in data if d["username"] != arg]
        with open("data.txt", "w") as file:
                json.dump(new_data, file)
        await ctx.send(f"> Player **{arg}** has been removed from the waiting list") 
    else:
        await ctx.send("This bot is not allowed to be used in this channel!")

@bot.command(name="list")
async def _list(ctx):

    if ctx.channel.id == int(config.get("bot", "channelID")):
        with open("data.txt") as file:
            waitlist = json.load(file)

        sort = sorted(waitlist, key=itemgetter("time"))

        output = ""
        for value in sort:
            output += str(value["username"]) + " | " + str(datetime.fromtimestamp(value["time"])) + "\n"

        list_embed = discord.Embed(
        title = "The Dawns Awakening - Waiting list",
        description = output,
        colour = 0xff55ff
        )
        list_embed.set_footer(text="All times are in (UTC)")
        await ctx.send(embed=list_embed)
    else:
        await ctx.send("This bot is not allowed to be used in this channel!")

@bot.command(name="help")
async def help(ctx):

    if ctx.channel.id == int(config.get("bot", "channelID")):
        help_embed = discord.Embed(title="The Dawns Awakening - Waiting list", colour=0xff55ff)
        help_embed.add_field(name="Help", value="\"" + config.get("bot","commandPrefix") + "help\" Shows this message", inline=False)
        help_embed.add_field(name="Add", value="\"" + config.get("bot","commandPrefix") + "add {username}\" will add a player to the waiting list", inline=True)
        help_embed.add_field(name="Remove", value="\"" + config.get("bot","commandPrefix") +"remove {username}\" will remove a player from the waiting list", inline=True)
        help_embed.add_field(name="List", value="\"" + config.get("bot","commandPrefix") + "list\" Will show the current waiting list", inline=True)
        await ctx.send(embed=help_embed)
    else:
        await ctx.send("This bot is not allowed to be used in this channel!")

bot.run(TOKEN)