import discord, toml
from discord.ext import commands
from scraper_class import Scraper

config = toml.load("config.toml")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_correct_channel():
    async def predicate(ctx):
        return ctx.channel.id == config['discord']['channel_id'] or ctx.channel.id == config['discord']['debug_channel_id']
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"Success!!! logged in as {bot.user}")

@bot.command()
@is_correct_channel()
async def get_points(ctx, faction, unit):
    await ctx.send(f"Searching for {unit}, from the {faction}")
    scraper = Scraper(faction)
    points = scraper.collect_points(scraper.scrape(unit))
    if points == 0:
        await ctx.send(f"{unit} couldn't be found checking other names.....")
        points_check =  scraper.collect_points_name_retry(unit)
        if points_check[0] == 0:
            await ctx.send(f"{unit} couldn't be found under any simmillar names.")
        else:
            await ctx.send(f"{points_check[1]} was found! it is {points} points.")
    else:
        await ctx.send(f"{unit} is {points} points.")
    

bot.run(config['discord']['token'])
