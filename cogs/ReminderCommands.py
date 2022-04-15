from discord.ext import commands, tasks
from discord.utils import get
from connect_to_db import db
from descriptions import *
from my_functions import *
import discord

class ReminderCommands(commands.Cog, name='Reminder Commands'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.channel.send(embed=embed('Theres been an error!', "That reminder doesn't exist."))
            return
            
        await ctx.channel.send(embed=embed('Theres been an error!', error))
        
    @commands.command(description=addReminderDescription)
    async def addreminder(self, ctx, reminderName, reminderMessage, reminderInterval):
        reminderName = reminderName.strip()
        minutesInADay = 1440
        reminderInterval = int(reminderInterval)
        
        if not (1 < reminderInterval < minutesInADay):
            return await ctx.channel.send('Reminder must be between 2 minutes and 1440 minutes.')
        if not (0 < len(reminderName) < 200):
            return await ctx.channel.send(embed=embed('', 'Reminder name must be shorter.'))
        if bool(getSingleReminder({'ReminderName': reminderName})):
            return await ctx.channel.send(embed=embed('', 'Reminder name must be unique.'))

        reminderRoleObject = await createReminderRole(ctx)
        reminderDeletionRoleObject = await createReminderDeletionRole(ctx, reminderName)
        reminderRoleID = reminderRoleObject.id
        reminderDeletionRoleID = reminderDeletionRoleObject.id

        reminder = {
            "ReminderName": reminderName,
            "ReminderMessage": reminderMessage,
            "ChannelID": ctx.channel.id,
            "ReminderInterval": reminderInterval,
            "AlreadySentThisMinute": 'False',
            "ReminderRoleID":reminderRoleID,
            "GuildID": ctx.guild.id,
            "DeletionRoleID": reminderDeletionRoleID
        }
                    
        db.insert_one(reminder)
        await ctx.send(embed=embed('','Reminder added!'))

    @commands.command(description=removeReminderRoleDescription)
    async def deletereminder(self, ctx, reminderName):
        reminderName = reminderName.strip()
        reminderDeletionRoleID = getSingleReminder({"ReminderName": reminderName})['DeletionRoleID']
        reminderDeletionRoleObject = get(ctx.author.roles, id=reminderDeletionRoleID)
        
        if bool(reminderDeletionRoleObject):
            reminderName = reminderName.strip()
            reminderRoleID = getSingleReminder({"ReminderName": reminderName})['ReminderRoleID']
            reminderRoleObject = get(ctx.guild.roles, id=reminderRoleID)
            db.delete_one({"ReminderName": reminderName})
            await reminderRoleObject.delete()
            await reminderDeletionRoleObject.delete()
            await ctx.channel.send(embed=embed('','Reminder has been deleted.'))
            return
            
        await ctx.channel.send(embed=embed('Missing Role','You need to have the deletion role for this reminder. The deletion role should have the same name as the reminder.'))
        
    @commands.command(description=addExistingReminderRoleDescription)
    async def addreminderrole(self, ctx, reminderName):
        reminderName = reminderName.strip()
        reminderRoleID = getSingleReminder({"ReminderName": reminderName})['ReminderRoleID']
        reminderRoleObject = get(ctx.guild.roles, id=reminderRoleID)
        await ctx.author.add_roles(reminderRoleObject)
        await ctx.channel.send(embed=embed('', 'Added the reminder role to you!'))
            
    @commands.command(description=removeExistingReminderRoleDescription)
    async def removereminderrole(self, ctx, reminderName):
        reminderName = reminderName.strip()
        reminderRoleID = getSingleReminder({"ReminderName": reminderName})['ReminderRoleID']
        reminderRoleObject = get(ctx.guild.roles, id=reminderRoleID)
        await ctx.author.remove_roles(reminderRoleObject)
        await ctx.channel.send(embed=embed('', 'Removed the reminder role from you!'))

    @commands.command(description=getAllRemindersForGuildDescription)
    async def getallreminders(self, ctx):
        allRemindersString = ""
        for reminder in getListOfReminders({"GuildID": ctx.guild.id}):
            allRemindersString += f"{reminder['ReminderName']}\n"
        await ctx.channel.send(embed=embed('List of Reminders', allRemindersString))
        
    @commands.command(description=getReminderDeletionRoleDescription)
    async def getreminderdeletionrole(self, ctx, reminderName):
        reminderName = reminderName.strip()
        reminderDeletionRoleID = getSingleReminder({"ReminderName": reminderName})['DeletionRoleID']
        reminderDeletionRoleObject = get(ctx.guild.roles, id=reminderDeletionRoleID)
        await ctx.channel.send(embed=embed(reminderName, f'{reminderDeletionRoleObject}'))

def setup(bot):
    bot.add_cog(ReminderCommands(bot))