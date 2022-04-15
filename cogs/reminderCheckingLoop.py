from discord.ext import commands, tasks
from discord.utils import get
from connect_to_db import db
from my_functions import *
import discord

#I realize I could do something where I create task.loops based off of the reminders, but this works well enough.

class checkReminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkReminders.start()
        
    @tasks.loop(seconds=10)
    async def checkReminders(self):
        listOfReminders = getListOfReminders()
        
        if bool(listOfReminders):
            totalTimeIntoTheDay = getTotalTimeIntoTheDay()
            minutesInADay = 1440
    
            for reminder in listOfReminders:
                reminderKeys = reminder.keys()
                _id, reminderName, reminderMessage, reminderChannelID, reminderInterval, alreadySentThisMinute, reminderRoleID, reminderGuildID, reminderDeletionRoleID = [reminder[key] for key in reminderKeys]
                
                if eval(alreadySentThisMinute):
                    if not  totalTimeIntoTheDay % reminderInterval == 0:
                        db.update_one(reminder, {"$set": { "AlreadySentThisMinute": "False" }})
                    return
                    
                if totalTimeIntoTheDay % reminderInterval == 0:
                    reminderChannelObject = self.bot.get_channel(reminderChannelID)
                    reminderGuildObject = self.bot.get_guild(reminderGuildID)
                    reminderRoleObject = get(reminderGuildObject.roles, id=reminderRoleID)

                    await reminderChannelObject.send(embed=embed(reminderName, reminderMessage))
                    db.update_one(reminder, {"$set": { "AlreadySentThisMinute": "True" }})
                    await reminderChannelObject.send(f"{reminderRoleObject.mention}")
    
def setup(bot):
    bot.add_cog(checkReminders(bot))