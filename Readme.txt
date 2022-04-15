This Discord.py bot sends reminders every x amount of minutes throughout the day.

Dependencies:
  pymongo
  discord.py
  flask
  dnspython
  
Commands List:
  Add Reminder Command: 
    Creates a reminder.
    Example: +addreminder "Example Reminder" "This is an example" 60

  Delete Reminder Command:
    Deletes a reminder.
    Example:+deletereminder "Example Reminder"

  Add Reminder Role Command:
    Adds the role for a reminder so that you get mentioned when the reminder is sent.
    Example: +addreminderrole "Example Reminder"

  Remove Reminder Role Command:
    Removes the reminder role so you are no longer mentioned when the reminder is sent.
    Example: +removereminderrole "Example Reminder"

  Get Reminder Deletion Role Command:
    You need a specific role to delete reminders. The reminder creator has it, and admins can add it to themselves.
    +getreminderdeletionrole

  Get All Reminders Command:
    Gets all reminders for a guild.
    +getallreminders
