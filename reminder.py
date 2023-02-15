import lightbulb
import hikari
from dotenv import load_dotenv
import os
import pickle
import datetime
from utils import get_formatted_date_from_unix, next_bd_unix
birthdays = pickle.load(open("birthdays.pickle", "rb"))

load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(int(os.environ["DEFAULT_GUILD"]),),
)
CHANNEL_ID = 832701526321397840

remind_time = pickle.load(open("remind.pickle", "rb"))

@bot.listen()
async def on_start(event: hikari.StartedEvent) -> None:
    #Check if any of the birthdays are within the next remind_time days
    for birthday in birthdays:
        #get the next birthday
        print(birthday)
        next_bd = next_bd_unix(birthday["Month"], birthday["Day"])
        #check if it is within the next remind_time days
        if next_bd - int(datetime.datetime.now().timestamp()) < remind_time * 86400:
            #check if there was a previous reminder
            if birthday["Last_Reminded"] != 0:
                #check if the previous reminder was within the last remind_time days
                if int(datetime.datetime.now().timestamp()) - birthday["Last_Reminded"] < remind_time * 86400:
                    #if so, skip this birthday
                    continue
            #if there was no previous reminder or the previous reminder was more than remind_time days ago, send a reminder
            user = await bot.rest.fetch_user(birthday["User"])
            await bot.rest.create_message(CHANNEL_ID, f"**{user.username}'s birthday is <t:{next_bd}:R>!!** :tada::tada::tada: ({get_formatted_date_from_unix(next_bd)[:-5]})\nMake sure to congratulate them!")
            #update the last reminded time
            birthday["Last_Reminded"] = int(datetime.datetime.now().timestamp())
    #shut down the bot
    await bot.close()
bot.run()