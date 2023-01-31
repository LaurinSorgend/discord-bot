import hikari
import lightbulb
from dotenv import load_dotenv
import os
import pickle
import datetime

load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=(int(os.environ["DEFAULT_GUILD"]),),
)

birthdays = pickle.load(open("birthdays.pickle", "rb"))

@bot.command
@lightbulb.command("birthday", "command group to store everyones birthdays")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def birthday(ctx: lightbulb.context) -> None:
    pass

@birthday.child
@lightbulb.option("day", "The day you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("year", "The year you were born", int)
@lightbulb.command("add", "add your birthday to the list")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.context) -> None:
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if year < 1900:
        await ctx.respond(f"{mention} only years before 1900! are allowed")
        return
    if month < 1 or month > 12:
        await ctx.respond(f"{mention} only months between 1 and 12 are allowed")
        return
    if day < 1 or day > 31:
        await ctx.respond(f"{mention} only days between 1 and 31 are allowed")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                await ctx.respond(f"{mention} you already have a birthday set! use /birthday change to change it!")
                return

    birthday = {"Guild": guild, "User": user, "Year": year, "Month": month, "Day": day}
    birthdays.append(birthday)

    pickle.dump(birthdays, open("birthdays.pickle", "wb"))

    await ctx.respond(f"{mention} your Birthday ({year}/{month}/{day}) has been added!")

@birthday.child
@lightbulb.option("year", "The year you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("day", "The day you were born", int)
@lightbulb.command("change", "change your birthday")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def change(ctx: lightbulb.context) -> None:
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if year < 1900:
        await ctx.respond(f"{mention} only years after 1900 are allowed!")
        return
    if month < 1 or month > 12:
        await ctx.respond(f"{mention} only months between 1 and 12 are allowed")
        return
    if day < 1 or day > 31:
        await ctx.respond(f"{mention} only days between 1 and 31 are allowed")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                i["Year"] = year
                i["Month"] = month
                i["Day"] = day

                pickle.dump(birthdays, open("birthdays.pickle", "wb"))

                await ctx.respond(f"{mention} your Birthday ({year}/{month}/{day}) has been changed!")
                return

    await ctx.respond(f"{mention} you don't have a birthday set! use /birthday add to add it!")

@birthday.child
@lightbulb.command("remove", "remove your birthday")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.context) -> None:
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                birthdays.remove(i)

                pickle.dump(birthdays, open("birthdays.pickle", "wb"))

                await ctx.respond(f"{mention} your Birthday has been removed!")
                return

    await ctx.respond(f"{mention} you don't have a birthday set! use /birthday add to add it!")

def get_formatted_date(year: int, month: int, day:int) -> str:
    months_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    full_day = str(day)
    if day == 1 or day == 21 or day == 31:
        full_day += "st"
    elif day == 2 or day == 22:
        full_day += "nd"
    elif day == 3 or day == 23:
        full_day += "rd"
    else:
        full_day += "th"
    return f"{full_day} of {months_names[month - 1]} {year}"

# convert to unix time, if the birthday is in the past, add a year
def convert_to_unix(month: int, day: int) -> int:
    # get current year
    current_year = datetime.datetime.now().year
    #if the birthday is in the past, add a year
    if datetime.datetime.now().month > month or (datetime.datetime.now().month == month and datetime.datetime.now().day > day):
        current_year += 1
    # convert to unix time
    return int(datetime.datetime(current_year, month, day).timestamp())

@birthday.child
@lightbulb.command("list", "list all birthdays")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.context) -> None:
    guild = ctx.guild_id
    birthdays_list = []

    for i in birthdays:
        if i["Guild"] == guild:
            user = await bot.rest.fetch_user(i["User"])
            birthdays_list.append(f"**{user.username}** - {get_formatted_date(i['Year'], i['Month'], i['Day'])} <t:{convert_to_unix(i['Month'], i['Day'])}:R>")

    if not birthdays_list:
        await ctx.respond("There are no birthdays set!")
        return

    await ctx.respond("**Birthdays:**\n" + "\n".join(birthdays_list))

bot.run()
