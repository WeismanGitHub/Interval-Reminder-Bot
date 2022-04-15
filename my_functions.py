from datetime import datetime
from discord.utils import get
from connect_to_db import db
import discord

blurple = 0x7289da
darkRedColor = 0x992d22

def embed(title, message, color=blurple):
    return discord.Embed(title = title, description = message, color=color)

async def createReminderRole(ctx):
    #250 because thats the role limit
    for i in range(1, 250):
        reminderRoleObject = get(ctx.guild.roles, name=f'IntervalReminderRole {i}')
        
        if not bool(reminderRoleObject):
            reminderRoleObject = await ctx.guild.create_role(name=f'IntervalReminderRole {i}')
            await ctx.author.add_roles(reminderRoleObject)
            return reminderRoleObject
            break
    await ctx.send(embed=embed('Delete Some Roles', "You've reached the 250 role limit."))


async def createReminderDeletionRole(ctx, reminderName):
    reminderDeletionRoleObject = await ctx.guild.create_role(name=f'{reminderName} Deletion Role')
    await ctx.author.add_roles(reminderDeletionRoleObject)
    return reminderDeletionRoleObject
    
def getListOfReminders(searchObject={}):
    return list(db.find(searchObject))

def getSingleReminder(requirementObject={}):
    reminder = db.find_one(requirementObject)
    return reminder if reminder != None else {}

def getTotalTimeIntoTheDay():
    minutesIntoTheDay = int(str(datetime.utcnow())[14:16].lstrip('0')) if str(datetime.utcnow())[14:16].lstrip('0') != '' else 0
    hoursIntoTheDay = int(str(datetime.utcnow())[11:13].lstrip('0')) if str(datetime.utcnow())[11:13].lstrip('0') != '' else 0
    totalTimeIntoTheDay = (60 * hoursIntoTheDay) + minutesIntoTheDay
    return totalTimeIntoTheDay