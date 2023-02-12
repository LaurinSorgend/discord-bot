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

# convert to unix time, if the birthday is in the past, add a year
def next_bd_unix(month: int, day: int) -> int:
    """gives the unix time of the next time the birthday will happen

    Args:
        month (int): month of the birthday
        day (int): day of the birthday

    Returns:
        int: unix time of the next birthday
    """
    # get current year
    current_year = datetime.datetime.now().year
    # if the birthday is in the past, add a year
    if datetime.datetime.now().month > month or (datetime.datetime.now().month == month and datetime.datetime.now().day > day):
        current_year += 1
    # convert to unix time
    return int(datetime.datetime(current_year, month, day).timestamp())


def get_formatted_date(year: int, month: int, day: int) -> str:
    """ converts the date to a string

    Args:
        year (int): year
        month (int): month
        day (int): day

    Returns:
        str: formatted date
    """
    months_names = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
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


def check_if_valid_date(year: int, month: int, day: int) -> bool:
    """checks if the date is valid (year is between 1900 and the current year, month is between 1 and 12, day is between 1 and 31)

    Args:
        year (int): year
        month (int): month
        day (int): day

    Returns:
        bool: True if the date is valid, False if not
    """
    if year > 1900 & year < datetime.datetime.now().year:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    return True


@bot.command
@lightbulb.command("birthday", "command group to store everyones birthdays")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def birthday(ctx: lightbulb.context) -> None:
    pass


@birthday.child
@lightbulb.option("year", "The year you were born", int)
@lightbulb.option("month", "The month you were born", int)
@lightbulb.option("day", "The day you were born", int)
@lightbulb.command("add", "add your birthday to the list")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.context) -> None:
    """adds a birthday to the list

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if not check_if_valid_date(year, month, day):
        await ctx.respond(f"{mention} the date you entered is not valid!")
        return

    for i in birthdays:
        if i["User"] == user:
            if i["Guild"] == guild:
                await ctx.respond(f"{mention} you already have a birthday set! use /birthday change to change it!")
                return

    birthday = {"Guild": guild, "User": user,
                "Year": year, "Month": month, "Day": day}
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
    """changes the birthday of a user

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    mention = ctx.author.mention
    user = int(mention[2:-1])
    year = ctx.options.year
    month = ctx.options.month
    day = ctx.options.day

    if not check_if_valid_date(year, month, day):
        await ctx.respond(f"{mention} the date you entered is not valid!")
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
    """removes a birthday from the list

    Args:
        ctx (lightbulb.context): context of the command
    """
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


@birthday.child
@lightbulb.command("list", "list all birthdays")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.context) -> None:
    """lists all birthdays

    Args:
        ctx (lightbulb.context): context of the command
    """
    guild = ctx.guild_id
    birthdays_list = []

    for i in birthdays:
        if i["Guild"] == guild:
            user = await bot.rest.fetch_user(i["User"])
            birthdays_list.append(
                f"**{user.username}** - {get_formatted_date(i['Year'], i['Month'], i['Day'])} <t:{next_bd_unix(i['Month'], i['Day'])}:R>")

    if not birthdays_list:
        await ctx.respond("There are no birthdays set!")
        return

    await ctx.respond("**Birthdays:**\n" + "\n".join(birthdays_list))


@birthday.child
@lightbulb.command("help", "Help for the birthday command group")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def help(ctx: lightbulb.context) -> None:
    """help for the birthday command group

    Args:
        ctx (lightbulb.context): context of the command
    """
    await ctx.respond("`/birthday add` - add your birthday.\n`/birthday change` - change your birthday.\n`/birthday remove` - remove your birthday.\n`/birthday list` - list all birthdays.\n`/birthday help` - get this message.")


bot.run()
