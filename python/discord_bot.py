import discord, toml, io, asyncio
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

def is_faction_none():
    async def checker(ctx):
        if ctx.bot.agent.faction is not None:
            return True
        
        # Send message directly
        await ctx.send("❌ Error: No faction has been assigned to the bot yet.")
        return False
        
    return commands.check(checker)

@bot.event
async def on_ready():
    print(f"Success!!! logged in as {bot.user}")

@bot.command()
@is_correct_channel()
async def man(ctx):
    await ctx.send(
    "### 📖 Bot Manual (Man Page)\n"
    "> *Note: If a unit or army name has a space, wrap it in double quotes (e.g., `\"Space Marines\"`)*\n"
    "```yaml\n"
    "# FACTION COMMANDS\n"
    "!check_stats <faction>      : Check stats for a faction\n"
    "!check_stats list_factions  : List all available factions\n"
    "!set_faction <name>         : Set your active faction\n"
    "!check_units                : View all units in your current faction\n"
    "!get_points <unit>          : Get points for a specific unit\n\n"
    "# ARMY LIST BUILDER\n"
    "!army_list current_army     : View your current army list\n"
    "!army_list add_unit         : Add a unit (starts interactive prompt)\n"
    "!army_list remove_unit      : Remove a unit from your list\n"
    "!army_list clear_list       : Wipe your entire list\n"
    "```"
)
    
@bot.command()
@is_correct_channel()
async def check_stats(ctx, stat):
    if stat.lower() == "faction":
        await ctx.send(f"Your current faction is {ctx.bot.agent.faction}")
    if stat.lower() == "list_factions":
        formatted_list = "\n".join([f"• {faction}" for faction in ctx.bot.agent.factions_list])
        await ctx.send(f"**Available Warhammer AoS Factions:**\n```text\n{formatted_list}\n```")

@bot.command()
@is_correct_channel()
async def set_faction(ctx, faction):
    ctx.bot.agent.faction = faction
    await ctx.send(f"Faction has been set to {faction}")

@bot.command()
@is_correct_channel()
@is_faction_none()
async def check_units(ctx):
    scraper = Scraper(ctx.bot.agent.faction)
    units = scraper.collect_faction_units()
    formatted_list = "\n".join([f"• {unit}" for unit in units])
    await ctx.send(f"**Available {ctx.bot.agent.faction} units:**\n```text\n{formatted_list}\n```")

@bot.command()
@is_correct_channel()
@is_faction_none()
async def get_points(ctx, unit):
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
@is_faction_none()
async def army_list(ctx, option):
    if option == "current_army":
        formatted_list = "\n".join([f"• {army}" for army in ctx.bot.agent.current_army_list])
        await ctx.send(f"**Current Army List:**\n```text\n{formatted_list}\n```")
        await ctx.send(f"Current Army Points: {ctx.bot.agent.current_army_points}")
    if option == "add_unit":
        await ctx.send(f"What unit from the {ctx.bot.agent.faction} would you like to add")

        # This check ensures only the person who ran the command can answer
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Wait for 30 seconds for a response
            msg = await ctx.bot.wait_for('message', check=check, timeout=30.0)
            
            unit_name = msg.content
            if unit_name.lower() == 'cancel':
                return await ctx.send("Unit addition cancelled.")

            scraper = Scraper(ctx.bot.agent.faction)
            points = scraper.collect_points(scraper.scrape(msg.content))
            
            if points != 0:
                ctx.bot.agent.current_army_list.append([unit_name, points])
                ctx.bot.agent.current_army_points += points
                await ctx.send(f"✅ Successfully added **{unit_name}** to your army list!")
            else:
                await ctx.send(f"❌ Failed adding **{unit_name}** to your army list! Check units for spellings")

        except asyncio.TimeoutError:
            await ctx.send("⏳ You took too long to respond. Command timed out.")
    if option == "drop_unit":
        await ctx.send(f"What unit from the {ctx.bot.agent.faction} would you like to remove")

        # This check ensures only the person who ran the command can answer
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            # Wait for 30 seconds for a response
            msg = await ctx.bot.wait_for('message', check=check, timeout=30.0)
            
            unit_name = msg.content
            if unit_name.lower() == 'cancel':
                return await ctx.send("Unit addition cancelled.")

            for i, sublist in enumerate(ctx.bot.agent.current_army_list):
                if sublist[0] == msg.content:
                    ctx.bot.agent.current_army_list.pop(i)  # Remove the item at this specific index
                    ctx.bot.agent.current_army_points -= sublist[1]
                    break
            await ctx.send(f"✅ Successfully removed **{unit_name}** from your army list!")

        except asyncio.TimeoutError:
            await ctx.send("⏳ You took too long to respond. Command timed out.")
    if option == "clear_list":
        ctx.bot.agent.current_army_list = []
        ctx.bot.agent.current_army_points = 0
        await ctx.send(f"✅ Successfully cleared army list!")

bot.run(config['discord']['token'])
