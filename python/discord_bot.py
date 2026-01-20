import discord, toml, io
from discord.ext import commands
from scraper_class import Scraper
import pandas as pd
from discord_agent import Agent

config = toml.load("config.toml")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.agent = Agent()

def is_correct_channel():
    async def predicate(ctx):
        return ctx.channel.id == config['discord']['channel_id']
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"Success!!! logged in as {bot.user}")

@bot.command()
@is_correct_channel()
async def man(ctx):
    await ctx.send(f"This is the man page hopefully it helps, remeber if your using a unit or army with a space wrap it in ""\nYou can check you current faction with or check all factions: !check_stats <faction/list_factions>\nYou can set a faction with: !set_faction <faction name>\nYou can check all units in a faction with: !check_units\nYou can check the points for a unit in your set faction with: !get_points <unit>")

@bot.command()
@is_correct_channel()
async def check_stats(ctx, stat):
    if stat.lower() == "faction":
        await ctx.send(f"Your current faction is {ctx.bot.agent.faction}")
    if stat.lower() == "list_factions":
        formatted_list = "\n".join([f"• {faction}" for faction in ctx.bot.agent.factions_list])
        await ctx.send(f"**Available Warhammer AoS Factions:**\n```text\n{formatted_list}\n```")
    if stat.lower() == "current_army":
        formatted_list = "\n".join([f"• {army}" for army in ctx.bot.agent.current_army_list])
        await ctx.send(f"**Current Army List:**\n```text\n{formatted_list}\n```")

@bot.command()
@is_correct_channel()
async def set_faction(ctx, faction):
    ctx.bot.agent.faction = faction
    await ctx.send(f"Faction has been set to {faction}")

@bot.command()
@is_correct_channel()
async def check_units(ctx):
    if ctx.bot.agent.faction == None:
        await ctx.send(f"Your faction is None run !set_faction <faction name>")
    scraper = Scraper(ctx.bot.agent.faction)
    units = scraper.collect_faction_units()
    formatted_list = "\n".join([f"• {unit}" for unit in units])
    await ctx.send(f"**Available {ctx.bot.agent.faction} units:**\n```text\n{formatted_list}\n```")

@bot.command()
@is_correct_channel()
async def get_points(ctx, unit):
    if ctx.bot.agent.faction == None:
        await ctx.send(f"Your faction is None run !set_faction <faction name>")
    await ctx.send(f"Searching for {unit}, from the {ctx.bot.agent.faction}")
    scraper = Scraper(ctx.bot.agent.faction)
    points = scraper.collect_points(scraper.scrape(unit))
    if points == 0:
        await ctx.send(f"{unit} couldn't be found checking other names.....")
        points_check =  scraper.collect_points_name_retry(unit)
        if points_check[0] == 0:
            await ctx.send(f"{unit} couldn't be found under any simmillar names.")
        else:
            await ctx.send(f"{points_check[1][0]} was found! it is {points_check[0]} points.")
    else:
        await ctx.send(f"{unit} is {points} points.")

@bot.command()
@is_correct_channel()
async def build_list(ctx):
    print("coming soon")

bot.run(config['discord']['token'])
