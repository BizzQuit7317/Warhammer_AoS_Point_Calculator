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
        return ctx.channel.id == config['discord']['channel_id'] or ctx.channel.id == config['discord']['debug_channel_id']
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"Success!!! logged in as {bot.user}")

@bot.command()
@is_correct_channel()
async def check_stats(ctx):
    await ctx.send(f"Your current faction is {ctx.bot.agent.faction}")

@bot.command()
@is_correct_channel()
async def set_faction(ctx, faction):
    ctx.bot.agent.faction = faction
    await ctx.send(f"Faction has been set to {faction}")


@bot.command()
@is_correct_channel()
async def get_points(ctx, unit):
    if ctx.bot.agent.faction == None:
        await ctx.send(f"Your faction is None run !set_faction <faction name>")
    debug_channel = bot.get_channel(config['discord']['debug_channel_id'])
    await ctx.send(f"Searching for {unit}, from the {ctx.bot.agent.faction}")
    scraper = Scraper(ctx.bot.agent.faction)
    points = scraper.collect_points(scraper.scrape(unit))
    if points == 0:
        await ctx.send(f"{unit} couldn't be found checking other names.....")
        points_check =  scraper.collect_points_name_retry(unit)
        if points_check[0] == 0:
            await ctx.send(f"{unit} couldn't be found under any simmillar names.")
            await debug_channel.send(f"[DBG][START]")
            await debug_channel.send(f"[DBG]Issue looking for faction: {ctx.bot.agent.faction}, unit: {unit}, other names checked: ")
            for name in points_check[1]:
                await debug_channel.send(f"[DBG]{name}")
            await debug_channel.send(f"[DBG][END]")
        else:
            await ctx.send(f"{points_check[1][0]} was found! it is {points_check[0]} points.")
    else:
        await ctx.send(f"{unit} is {points} points.")

"""
Bring this back as needed when error are occuring

@bot.command()
@is_correct_channel()
async def fetch_logs(ctx):
    debug_channel = bot.get_channel(config['discord']['debug_channel_id'])
    lines = []
    async for message in debug_channel.history(limit=10000): #10k is arbitrary number of logs a long ass the csv iss ssmaller than 25MB
        if message.content.startswith("[DBG]"):
            lines.append(message.content)
    await ctx.send(f"Generating CSV file....")
    gather_logs(lines)
    with open("error_point_names.csv", "rb") as f:
        file_to_upload = discord.File(f, filename="error_point_names.csv")
        await ctx.send("CSV file generated.", file=file_to_upload)


def gather_logs(lines):
    dbg_blocks = []
    current_block = {}  # Start with an empty dictionary
    end_flag = False
    var_counter = 0

    for text in lines:
        if text == "[DBG][START]":
            # If we have data in current_block, save it before starting a new one
            if current_block:
                dbg_blocks.append(current_block)
            current_block = {} # Reset to a fresh dict
            end_flag = False
            var_counter = 0
            continue # Skip to next line

        if text == "[DBG][END]":
            end_flag = True
            continue

        if end_flag:
            if "faction:" in text and "unit:" in text:
                # Create a small temp dict for the new data
                new_data = {
                    "faction": text.split("faction: ")[1].split(",")[0], 
                    "unit": text.split("unit: ")[1].split(",")[0]
                }
            else:
                clean_text = text.replace("DBG", "").replace("[", "").replace("]", "")
                new_data = {f"unit_vars{var_counter}": clean_text}
                var_counter += 1
            
            # MERGE into the current block immediately
            current_block.update(new_data)

    # Don't forget to append the very last block after the loop finishes
    if current_block:
        dbg_blocks.append(current_block)

    df = pd.DataFrame(dbg_blocks)

    priority_cols = ["faction", "unit"]
    other_cols = [c for c in df.columns if c not in priority_cols]
    other_cols.sort()

    final_column_order = [c for c in priority_cols if c in df.columns] + other_cols
    df = df[final_column_order]
    df.to_csv("error_point_names.csv", index=False)
"""

bot.run(config['discord']['token'])
