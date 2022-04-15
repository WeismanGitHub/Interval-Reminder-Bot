from keep_alive import keep_alive
from discord.ext import commands
import discord
import os

bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.load_extension("cogs.ReminderCommands")
    bot.load_extension("cogs.reminderCheckingLoop")
    activity = discord.Game(name="Drink Water")
    await bot.change_presence(activity=activity)
    
keep_alive()
bot.run(os.getenv('Token'))
