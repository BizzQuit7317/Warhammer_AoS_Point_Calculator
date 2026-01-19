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
    debug_channel = bot.get_channel(config['discord']['debug_channel_id'])
    await ctx.send(f"Searching for {unit}, from the {faction}")
    scraper = Scraper(faction)
    points = scraper.collect_points(scraper.scrape(unit))
    if points == 0:
        await ctx.send(f"{unit} couldn't be found checking other names.....")
        points_check =  scraper.collect_points_name_retry(unit)
        if points_check[0] == 0:
            await ctx.send(f"{unit} couldn't be found under any simmillar names.")
            await debug_channel.send(f"[DBG][START]")
            await debug_channel.send(f"[DBG]Issue looking for faction: {faction}, unit: {unit}, other names checked: ")
            for name in points_check[1]:
                await debug_channel.send(f"[DBG]{name}")
            await debug_channel.send(f"[DBG][END]")
        else:
            await ctx.send(f"{points_check[1][0]} was found! it is {points_check[0]} points.")
    else:
        await ctx.send(f"{unit} is {points} points.")

@bot.command()
@is_correct_channel()
async def fetch_logs(ctx):
    debug_channel = bot.get_channel(config['discord']['debug_channel_id'])
    async for message in debug_channel.history(limit=100):
        if message.content.startswith("[DBG]"):
            print(f"{message.content}")


bot.run(config['discord']['token'])
