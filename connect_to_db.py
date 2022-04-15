from pymongo import MongoClient
import os

client = MongoClient(f"mongodb+srv://{os.getenv('MongoUsername')}:{os.getenv('MongoPassword')}@cluster0.c5eyl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db=client.ReminderBotDatabase.reminders